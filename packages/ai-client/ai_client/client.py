from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Sequence, Union

from .errors import AIClientHTTPError, AIClientJSONError
from .types import AIMessage, AIRequestContext, AIResponse, AIUsage

MessagesInput = Union[str, Sequence[AIMessage]]


class AIClient:
    """Small internal client that forces app code through LiteLLM Proxy."""

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout_seconds: float = 60.0,
    ) -> None:
        self.base_url = (base_url or os.getenv("LITELLM_BASE_URL") or "http://localhost:4000").rstrip("/")
        self.api_key = (
            api_key
            or os.getenv("LITELLM_API_KEY")
            or os.getenv("LITELLM_MASTER_KEY")
            or "sk-local-dev"
        )
        self.timeout_seconds = timeout_seconds

    @classmethod
    def from_env(cls) -> "AIClient":
        return cls()

    def generate(
        self,
        messages: MessagesInput,
        *,
        context: AIRequestContext,
        model_profile: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 800,
        response_format: Optional[Dict[str, str]] = None,
    ) -> AIResponse:
        model = model_profile or context.model_profile
        payload: Dict[str, Any] = {
            "model": model,
            "messages": self._normalize_messages(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            "metadata": context.metadata(),
        }
        if context.user_id:
            payload["user"] = context.user_id
        if response_format:
            payload["response_format"] = response_format

        raw = self._post_json("/v1/chat/completions", payload)
        content = self._extract_content(raw)
        returned_model = str(raw.get("model") or model)
        return AIResponse(
            content=content,
            model=returned_model,
            usage=AIUsage.from_payload(raw),
            context=context,
            raw=raw,
        )

    def generate_json(
        self,
        messages: MessagesInput,
        *,
        context: AIRequestContext,
        model_profile: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 800,
    ) -> Dict[str, Any]:
        json_messages = self._normalize_messages(messages)
        json_messages.insert(
            0,
            {
                "role": "system",
                "content": "Return only valid JSON. Do not wrap it in Markdown.",
            },
        )
        response = self.generate(
            json_messages,
            context=context,
            model_profile=model_profile,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
        )
        try:
            parsed = json.loads(response.content)
        except json.JSONDecodeError as exc:
            raise AIClientJSONError(f"Model response was not valid JSON: {exc}") from exc
        if not isinstance(parsed, dict):
            raise AIClientJSONError("Model JSON response must be an object.")
        return parsed

    def judge(
        self,
        prompt: str,
        *,
        context: AIRequestContext,
        max_tokens: int = 600,
    ) -> Dict[str, Any]:
        return self.generate_json(
            prompt,
            context=context,
            model_profile="judge",
            temperature=0.0,
            max_tokens=max_tokens,
        )

    def build_payload_for_debug(
        self,
        messages: MessagesInput,
        *,
        context: AIRequestContext,
        model_profile: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> Dict[str, Any]:
        return {
            "url": self._url("/v1/chat/completions"),
            "model": model_profile or context.model_profile,
            "messages": self._normalize_messages(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            "metadata": context.metadata(),
        }

    def _post_json(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self._url(path),
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                response_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            response_body = exc.read().decode("utf-8", errors="replace")
            raise AIClientHTTPError(exc.code, exc.reason, response_body) from exc
        except urllib.error.URLError as exc:
            raise AIClientHTTPError(0, str(exc.reason)) from exc

        try:
            parsed = json.loads(response_body)
        except json.JSONDecodeError as exc:
            raise AIClientJSONError(f"LiteLLM returned invalid JSON: {exc}") from exc
        if not isinstance(parsed, dict):
            raise AIClientJSONError("LiteLLM response must be a JSON object.")
        return parsed

    def _url(self, path: str) -> str:
        if self.base_url.endswith("/v1") and path.startswith("/v1/"):
            return f"{self.base_url}{path[3:]}"
        return f"{self.base_url}{path}"

    @staticmethod
    def _normalize_messages(messages: MessagesInput) -> List[AIMessage]:
        if isinstance(messages, str):
            return [{"role": "user", "content": messages}]
        return [dict(message) for message in messages]

    @staticmethod
    def _extract_content(payload: Dict[str, Any]) -> str:
        choices = payload.get("choices")
        if not choices:
            return ""
        message = choices[0].get("message") or {}
        content = message.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return "\n".join(str(part.get("text", "")) for part in content if isinstance(part, dict))
        return ""
