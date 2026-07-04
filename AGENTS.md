# Project Guide for Codex

## Project

This repository is the course project for an enterprise AI incident and support platform.

The first lesson builds the local AI engineering foundation:

- LiteLLM Proxy as the model gateway.
- Codex as the local engineering assistant.
- `packages/ai-client` as the only supported path for model calls.

Later lessons add the ticket system, Agent Runtime, Tool Hub, RAG, and a hand-built AI Harness.

## Repository Layout

```text
infra/                  Local infrastructure and LiteLLM config
packages/ai-client/     Internal AI client used by all app code
packages/harness/       AI Harness, added in later lessons
packages/agent-runtime/ Agent execution layer, added in later lessons
packages/tool-hub/      Tool calling layer, added in later lessons
packages/rag/           Retrieval layer, added in later lessons
scripts/                Local smoke tests and developer scripts
prompts/                Versioned prompts, added in later lessons
tasks/                  Harness task specs, added in later lessons
```

## Hard Rules

- Do not call model providers directly from app, agent, tool, or harness code.
- All model calls must go through `packages/ai-client`.
- The app should call LiteLLM aliases such as `fast`, `smart`, `judge`, `code`, and `cheap`, not provider model ids.
- Do not commit `.env` or real API keys.
- Keep lesson code small and runnable; add complexity only when a later lesson needs it.

## Local Commands

Start local infrastructure:

```bash
docker compose -f infra/docker-compose.yml up -d
```

Run the AI client dry run without external API calls:

```bash
python3 scripts/smoke_ai_client.py --dry-run
```

Run the real LiteLLM smoke test after setting `.env`:

```bash
python3 scripts/smoke_ai_client.py
```

Basic Python syntax check:

```bash
python3 -m compileall packages scripts
```

## Completion Standard

For lesson 1 changes, verify at least:

```bash
python3 scripts/smoke_ai_client.py --dry-run
python3 -m compileall packages scripts
```

If Docker and a provider API key are available, also verify:

```bash
docker compose -f infra/docker-compose.yml up -d
python3 scripts/smoke_ai_client.py
```
