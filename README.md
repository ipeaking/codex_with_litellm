# 企业级 AI 工程实战：LiteLLM、Codex 与自研 Harness

这是一个面向有开发经验工程师的课程项目，目标是从零构建一个企业内部 AI 工单与故障处理平台。

项目不是普通 Chatbot，而是围绕企业级 AI 工程能力展开：

- 使用 LiteLLM 作为统一模型网关。
- 使用 Codex 作为本地工程协作者。
- 自研 Internal AI Client，避免业务代码直接依赖模型供应商。
- 后续课程会逐步实现工单系统、Agent Runtime、Tool Hub、RAG 和 AI Harness。
- 重点手搓 Harness，让 AI 行为可评测、可回放、可比较、可进入 CI Gate。

## 当前进度

当前代码对应课程第 1 课：

**搭建 LiteLLM + Codex 本地 AI 开发环境**

已经包含：

```text
LiteLLM Proxy 配置
Postgres / Redis / LiteLLM Docker Compose
Internal AI Client
Codex 项目规则
本地 smoke test
```

## 项目结构

```text
.
├── AGENTS.md
├── README.md
├── .codex/
│   └── config.toml
├── infra/
│   ├── docker-compose.yml
│   └── litellm/
│       └── config.yaml
├── packages/
│   └── ai-client/
│       ├── pyproject.toml
│       └── ai_client/
│           ├── __init__.py
│           ├── client.py
│           ├── errors.py
│           └── types.py
├── scripts/
│   └── smoke_ai_client.py
├── enterprise-ai-incident-architecture.md
├── enterprise-ai-incident-course-outline.md
└── enterprise-ai-incident-requirements.md
```

## 快速开始

## Docker 是否必需

不必需。

LiteLLM 可以作为 Python SDK 直接在代码中使用，也可以启动 Proxy Server 作为统一模型网关。课程默认使用 Docker Compose，是因为它能一次性拉起 LiteLLM、Postgres 和 Redis，适合教学录制和多人复现。

如果只想本地快速启动 LiteLLM Proxy，也可以不用 Docker：

```bash
uv tool install 'litellm[proxy]'
export OPENAI_API_KEY=你的 OpenAI API Key
export LITELLM_MASTER_KEY=sk-local-dev
litellm --config infra/litellm/config.yaml --host 0.0.0.0 --port 4000
```

然后另开一个终端运行：

```bash
python3 scripts/smoke_ai_client.py
```

本课程推荐：

```text
课程录制 / 学员复现 / 后续需要 Postgres 和 Redis：使用 Docker Compose
个人本地快速试验 / 只验证 LiteLLM Proxy：使用 LiteLLM CLI
只在 Python 代码中统一调用模型：可以使用 LiteLLM Python SDK
```

### 1. 准备环境变量

```bash
cp .env.example .env
```

然后编辑 `.env`，填入：

```text
OPENAI_API_KEY=你的 OpenAI API Key
LITELLM_MASTER_KEY=sk-local-dev
LITELLM_BASE_URL=http://localhost:4000
```

### 2. 启动本地基础设施

```bash
docker compose -f infra/docker-compose.yml up -d
```

这会启动：

```text
Postgres
Redis
LiteLLM Proxy
```

LiteLLM 默认监听：

```text
http://localhost:4000
```

### 3. 运行 dry run

dry run 不会真的调用模型，只会打印将要发送给 LiteLLM 的请求。

```bash
python3 scripts/smoke_ai_client.py --dry-run
```

### 4. 运行真实模型调用

确认 `.env` 中已经配置 `OPENAI_API_KEY` 后运行：

```bash
python3 scripts/smoke_ai_client.py
```

期望看到类似输出：

```text
Calling LiteLLM Proxy...
base_url=http://localhost:4000
model_profile=fast
trace_id=trace_xxx
response ok
returned_model=...
usage_total_tokens=...
content=...
```

## LiteLLM 模型别名

应用代码不直接使用供应商模型 ID，而是使用稳定的模型 profile：

```text
fast    轻量分类、摘要
smart   复杂分析、规划
judge   Eval judge
code    代码理解和修复
cheap   批量低成本任务
```

配置文件：

[infra/litellm/config.yaml](infra/litellm/config.yaml)

后续可以修改 alias 背后的真实模型，而不影响业务代码。

## Internal AI Client

所有模型调用都必须经过：

[packages/ai-client](packages/ai-client)

当前提供：

```text
generate()
generate_json()
judge()
```

每次请求都会携带：

```text
trace_id
run_id
task_id
model_profile
prompt_version
cost_center
user_id
team_id
```

这为后续 Harness 的 Trace、Replay、Eval 和成本治理打基础。

## Codex 使用约定

项目级规则写在：

[AGENTS.md](AGENTS.md)

Codex 项目配置写在：

[.codex/config.toml](.codex/config.toml)

重要约定：

- 不要在业务代码中直接调用模型供应商。
- 所有模型调用都走 `packages/ai-client`。
- 应用只使用 `fast`、`smart`、`judge`、`code`、`cheap` 等模型别名。
- 不提交 `.env` 或真实 API Key。

## 本地检查

```bash
python3 scripts/smoke_ai_client.py --dry-run
python3 -m compileall packages scripts
docker compose -f infra/docker-compose.yml config
```

## 课程文档

- [架构设计](enterprise-ai-incident-architecture.md)
- [需求文档](enterprise-ai-incident-requirements.md)
- [10 课课程大纲](enterprise-ai-incident-course-outline.md)

## 后续课程路线

```text
第 1 课：搭建 LiteLLM + Codex 本地 AI 开发环境
第 2 课：工单系统与 Agent Runtime 骨架
第 3 课：Tool Hub、Mock 工具与 Policy
第 4 课：跑通第一个端到端 AI 工单案例
第 5 课：手搓 Harness：Task Spec 与 Runner
第 6 课：手搓 Harness：Trace Recorder
第 7 课：手搓 Harness：Eval Checkers 与 LLM Judge
第 8 课：手搓 Harness：Tool Mock 与 Deterministic Replay
第 9 课：手搓 Harness：Compare、Regression Report 与 CI Gate
第 10 课：Codex Skills、失败 Trace 调试与完整项目演示
```
