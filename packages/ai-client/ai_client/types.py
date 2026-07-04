from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import uuid4

AIMessage = Dict[str, str]


@dataclass(frozen=True)
class AIRequestContext:
    trace_id: str
    run_id: str
    task_id: str
    model_profile: str
    prompt_version: str
    cost_center: str
    user_id: Optional[str] = None
    team_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        task_id: str,
        model_profile: str = "fast",
        prompt_version: str = "lesson-01",
        cost_center: str = "course-local-dev",
        user_id: Optional[str] = "local-user",
        team_id: Optional[str] = "course-team",
        run_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> "AIRequestContext":
        return cls(
            trace_id=trace_id or f"trace_{uuid4().hex}",
            run_id=run_id or f"run_{uuid4().hex}",
            task_id=task_id,
            model_profile=model_profile,
            prompt_version=prompt_version,
            cost_center=cost_center,
            user_id=user_id,
            team_id=team_id,
            extra=extra or {},
        )

    def metadata(self) -> Dict[str, Any]:
        base: Dict[str, Any] = {
            "trace_id": self.trace_id,
            "run_id": self.run_id,
            "task_id": self.task_id,
            "model_profile": self.model_profile,
            "prompt_version": self.prompt_version,
            "cost_center": self.cost_center,
        }
        if self.user_id:
            base["user_id"] = self.user_id
        if self.team_id:
            base["team_id"] = self.team_id
        base.update(self.extra)
        return base


@dataclass(frozen=True)
class AIUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "AIUsage":
        usage = payload.get("usage") or {}
        return cls(
            prompt_tokens=int(usage.get("prompt_tokens") or 0),
            completion_tokens=int(usage.get("completion_tokens") or 0),
            total_tokens=int(usage.get("total_tokens") or 0),
        )


@dataclass(frozen=True)
class AIResponse:
    content: str
    model: str
    usage: AIUsage
    context: AIRequestContext
    raw: Dict[str, Any]

    @property
    def messages(self) -> List[AIMessage]:
        return [{"role": "assistant", "content": self.content}]
