#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AI_CLIENT_SRC = ROOT / "packages" / "ai-client"
sys.path.insert(0, str(AI_CLIENT_SRC))

from ai_client import AIClient, AIRequestContext  # noqa: E402


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke test the local LiteLLM AI client.")
    parser.add_argument("--model-profile", default="fast", help="LiteLLM model alias to call.")
    parser.add_argument(
        "--prompt",
        default="用一句话说明企业 AI 系统为什么需要统一模型网关。",
        help="Prompt sent to the model.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request payload without calling LiteLLM.",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv(ROOT / ".env")
    args = parse_args()

    context = AIRequestContext.create(
        task_id="lesson-01-smoke-test",
        model_profile=args.model_profile,
        prompt_version="lesson-01-smoke-v1",
    )
    client = AIClient.from_env()

    if args.dry_run:
        print("LiteLLM smoke test dry run")
        print(f"base_url={client.base_url}")
        print(f"model_profile={args.model_profile}")
        print(f"trace_id={context.trace_id}")
        print(json.dumps(client.build_payload_for_debug(args.prompt, context=context), ensure_ascii=False, indent=2))
        return 0

    print("Calling LiteLLM Proxy...")
    print(f"base_url={client.base_url}")
    print(f"model_profile={args.model_profile}")
    print(f"trace_id={context.trace_id}")
    response = client.generate(args.prompt, context=context, max_tokens=300)
    print("response ok")
    print(f"returned_model={response.model}")
    print(f"usage_total_tokens={response.usage.total_tokens}")
    print(f"content={response.content}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
