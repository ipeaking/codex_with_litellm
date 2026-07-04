# 企业级 AI 工单与故障处理平台课程案例需求文档

## 1. 背景与定位

本课程案例面向有较多开发经验的工程师，目标不是做一个简单的 AI Chatbot，而是从零构建一个具备企业工程属性的 AI 平台案例。

项目以 **LiteLLM + Codex + 自研 AI Harness** 为核心：

- LiteLLM 负责统一模型网关、模型路由、成本统计、限流和 fallback。
- Codex 负责工程自动化、代码修复、测试执行、PR 辅助和项目工作流。
- 自研 AI Harness 负责 AI 行为的可复现、可评测、可回放、可比较和可治理。

课程最终产物是一个可运行、可演示、可扩展的企业内部 AI 工单与故障处理平台。

## 2. 项目目标

### 2.1 业务目标

构建一个企业内部 AI Copilot，用于处理以下类型的问题：

1. 企业内部知识问答。
2. 运维故障初步排查。
3. 历史工单和 Runbook 检索。
4. 日志、监控、CI、代码仓库等系统的信息聚合。
5. 代码级问题定位、修复建议和 PR 辅助。

### 2.2 工程目标

通过该项目训练高级开发者掌握：

1. 企业级 AI 应用的分层架构。
2. 多模型网关和模型治理。
3. Agent Runtime 的任务编排、工具调用和人工确认。
4. RAG 与企业知识库集成。
5. 自研 AI Harness 的设计与实现。
6. AI 任务的 trace、replay、eval、mock 和 regression。
7. Codex 在大型工程项目中的工作流化使用。
8. AI 系统的 CI Gate、审计、成本治理和可观测性。

## 3. 目标用户

### 3.1 平台使用者

- 企业员工：提交内部流程、权限、文档类问题。
- 后端工程师：查询代码、CI、日志、接口问题。
- SRE / 运维工程师：排查故障、查看监控、执行 Runbook。
- 技术负责人：查看 AI 处理质量、成本和风险。

### 3.2 课程学习者

- 具备后端开发经验的工程师。
- 熟悉 Python 或 TypeScript。
- 理解 HTTP API、数据库、消息队列、CI/CD。
- 希望系统学习企业级 AI 应用、Agent、Eval 和 Harness 的开发者。

## 4. 课程案例主线

课程案例围绕一个完整闭环展开：

```text
用户提交工单
-> Agent 分类和规划
-> 检索知识库 / Runbook / 历史工单
-> 调用日志、监控、CI、代码仓库等工具
-> 生成分析结果和处理建议
-> 高风险操作进入人工确认
-> Codex 辅助定位和修复代码
-> Harness 记录 trace
-> Harness replay / eval / compare
-> CI Gate 阻止退化版本上线
```

## 5. 范围定义

### 5.1 MVP 范围

MVP 必须完成以下能力：

1. Web Console：工单列表、工单详情、AI 处理结果、Trace 查看。
2. API/BFF：工单创建、查询、AI 任务触发。
3. Agent Runtime：任务分类、规划、工具调用、答案生成。
4. LiteLLM Proxy：统一模型调用。
5. Internal AI Client：封装模型请求，注入 trace、cost、metadata。
6. RAG Service：检索本地文档、Runbook、历史工单。
7. Tool Hub：至少实现日志、监控、代码搜索 3 类 mock 工具。
8. AI Harness Core：支持 run、replay、compare、report。
9. Trace Store：保存模型调用、工具调用、成本、耗时、结果。
10. Eval Dataset：至少 20 条 golden tasks。
11. CI Gate：在关键改动时运行 eval subset。

### 5.2 进阶范围

进阶阶段可增加：

1. 多租户、团队预算、成本看板。
2. 人工审批和高风险工具调用确认。
3. MCP Server 接入 GitHub、Jira、Prometheus、Loki。
4. Langfuse 或 OpenTelemetry 集成。
5. Judge 模型评测与人工复核。
6. Codex Skill 自动调试失败 trace。
7. Codex 辅助生成修复 PR。
8. Prompt 版本管理和 A/B 实验。
9. 真实 CI/CD 集成。
10. Failure Taxonomy 和自动归因。

## 6. 核心业务需求

### 6.1 工单管理

系统应支持用户创建和管理工单。

必需字段：

- 工单标题。
- 工单描述。
- 问题类型。
- 优先级。
- 环境信息。
- 关联服务。
- 附件。
- 提交人。
- 当前状态。

工单状态：

```text
open
-> triaging
-> waiting_for_approval
-> resolved
-> rejected
-> escalated
```

验收标准：

- 用户可以创建工单。
- 用户可以查看工单列表和详情。
- 工单可以触发 AI 分析。
- 工单详情中可以看到 AI 的结论、证据、工具调用和建议动作。

### 6.2 AI 工单分类

Agent 应根据工单内容自动分类：

- knowledge_question：知识问答。
- incident_triage：故障排查。
- ci_failure：CI 失败。
- code_bug：代码缺陷。
- access_request：权限/流程申请。
- unknown：无法判断。

验收标准：

- 分类结果必须包含 category、confidence、reason。
- confidence 低于阈值时进入人工确认。
- 分类过程必须被 trace 记录。

### 6.3 任务规划

Agent 应根据工单类型生成处理计划。

计划结构：

```json
{
  "goal": "定位登录服务 500 错误原因",
  "steps": [
    {
      "id": "step-1",
      "action": "search_runbook",
      "reason": "先查找登录服务相关 Runbook"
    }
  ],
  "risk_level": "medium",
  "needs_approval": false
}
```

验收标准：

- 每个计划必须包含 goal、steps、risk_level。
- 工具调用必须来自 allowlist。
- 高风险操作必须进入 approval。

### 6.4 工具调用

系统应支持通过 Tool Hub 调用企业内部系统。

MVP 工具：

| 工具 | 功能 |
| --- | --- |
| search_docs | 检索企业文档 |
| search_runbook | 检索故障处理手册 |
| search_tickets | 检索历史工单 |
| query_logs | 查询日志 |
| query_metrics | 查询监控指标 |
| search_code | 搜索代码 |
| get_ci_status | 查询 CI 状态 |

验收标准：

- 每次工具调用必须记录 input、output、latency、status。
- 工具调用失败时 Agent 必须能降级处理。
- 工具返回必须可被 Harness mock。

### 6.5 AI 分析结果

不同类型工单应输出结构化结果。

故障排查结果示例：

```json
{
  "summary": "登录服务 500 错误主要集中在 auth-service 的 token 校验路径",
  "suspected_root_cause": "新版本引入的空指针异常",
  "evidence": [
    "query_logs 返回 /auth/verify 出现 NullPointerException",
    "query_metrics 显示 10:05 后错误率上升",
    "CI 记录显示 auth-service 在 10:00 完成发布"
  ],
  "recommended_actions": [
    "回滚 auth-service 到 v1.8.2",
    "检查 TokenParser 的 null handling"
  ],
  "confidence": 0.82,
  "risk_level": "medium"
}
```

验收标准：

- 输出必须符合 JSON Schema。
- 结论必须引用证据。
- 高风险建议必须标记 risk_level。
- 低置信度结果必须建议人工接管。

## 7. AI Harness 需求

Harness 是课程案例的重点，需要手搓实现，而不是只接现成平台。

### 7.1 Harness 总体职责

Harness 必须支持：

1. 定义 AI 任务。
2. 执行 AI 任务。
3. 记录完整 trace。
4. 对历史任务 replay。
5. 对结果 eval。
6. 对 baseline 和 candidate compare。
7. mock 工具返回。
8. 生成报告。
9. 接入 CI Gate。

### 7.2 Harness CLI

必须实现以下命令：

```bash
ai-harness run tasks/incident-login-500.yaml
ai-harness run tasks/ --model smart --limit 20
ai-harness replay traces/2026-07-04/run-001.json
ai-harness compare runs/baseline runs/candidate
ai-harness report runs/candidate --format html
ai-harness list tasks/
ai-harness inspect traces/run-001.json
```

命令说明：

| 命令 | 功能 |
| --- | --- |
| run | 执行单个或多个 task |
| replay | 使用历史 trace 或 task 重新执行 |
| compare | 比较两组运行结果 |
| report | 生成 Markdown/HTML 报告 |
| list | 列出任务集 |
| inspect | 查看 trace 摘要 |

### 7.3 Task Spec

Task Spec 使用 YAML 定义。

示例：

```yaml
id: incident-login-500
name: 登录服务 500 错误排查
type: incident_triage
tags:
  - incident
  - auth-service
input:
  ticket_title: "登录服务 500 错误增多"
  ticket_description: "从 10:05 开始，登录接口 500 明显增多"
  environment: "prod"
  service: "auth-service"
tools:
  allowed:
    - search_runbook
    - query_logs
    - query_metrics
    - search_code
limits:
  max_steps: 8
  timeout_seconds: 120
  max_model_cost_usd: 0.30
expected:
  must_include:
    - suspected_root_cause
    - evidence
    - recommended_actions
  must_not_include:
    - "直接删除生产数据"
eval:
  checks:
    - schema
    - required_fields
    - evidence_citation
    - tool_usage
    - cost_limit
    - judge_factuality
```

验收标准：

- Task Spec 必须使用 Pydantic 或类似机制校验。
- 缺少关键字段时 CLI 应输出友好错误。
- limits 必须被 Runtime 强制执行。
- tools.allowed 必须被 Tool Hub 和 Policy 同时校验。

### 7.4 Trace Schema

Trace 必须保存一次 AI 任务的完整过程。

核心字段：

```json
{
  "trace_id": "trace_001",
  "task_id": "incident-login-500",
  "run_id": "run_20260704_001",
  "git_commit": "abc123",
  "model_profile": "smart",
  "started_at": "2026-07-04T10:00:00Z",
  "ended_at": "2026-07-04T10:00:30Z",
  "status": "passed",
  "spans": [],
  "usage": {
    "prompt_tokens": 1200,
    "completion_tokens": 600,
    "cost_usd": 0.08
  },
  "final_output": {},
  "eval_result": {}
}
```

Span 类型：

| Span Type | 说明 |
| --- | --- |
| agent.step | Agent 执行步骤 |
| model.call | 模型调用 |
| tool.call | 工具调用 |
| rag.retrieve | RAG 检索 |
| policy.check | 策略检查 |
| eval.check | 评测检查 |

验收标准：

- 每个 span 必须有 span_id、parent_span_id、type、started_at、ended_at、status。
- model.call 必须记录 model、provider、prompt_hash、token、cost。
- tool.call 必须记录 tool_name、input_hash、output_hash、latency。
- 原始敏感内容不能直接进入公开报告。

### 7.5 Tool Mock Server

为了保证 eval 可复现，Harness 必须支持工具 mock。

Mock 定义示例：

```yaml
task_id: incident-login-500
mocks:
  query_logs:
    input_match:
      service: auth-service
    output:
      entries:
        - timestamp: "2026-07-04T10:06:00Z"
          level: "ERROR"
          message: "NullPointerException at TokenParser.parse"
  query_metrics:
    output:
      error_rate: 0.18
      p95_latency_ms: 1200
```

验收标准：

- Harness run 支持 `--mock-tools`。
- Replay 默认优先使用历史工具返回。
- Mock 未命中时应明确报错或进入真实工具调用模式。
- Mock 结果也必须进入 trace。

### 7.6 Eval Checks

Harness 至少实现以下评测器：

| Check | 类型 | 说明 |
| --- | --- | --- |
| schema | 规则 | 验证输出 JSON Schema |
| required_fields | 规则 | 验证必填字段 |
| forbidden_text | 规则 | 禁止危险建议 |
| tool_usage | 规则 | 检查是否调用必要工具 |
| evidence_citation | 规则 | 结论是否引用证据 |
| cost_limit | 规则 | 是否超过成本限制 |
| latency_limit | 规则 | 是否超过耗时限制 |
| judge_factuality | LLM Judge | 判断结论是否被证据支持 |
| judge_helpfulness | LLM Judge | 判断建议是否有帮助 |
| regression | 对比 | 与 baseline 相比是否退化 |

评分结构：

```json
{
  "score": 0.86,
  "passed": true,
  "checks": [
    {
      "name": "schema",
      "passed": true,
      "score": 1.0,
      "reason": "输出符合 schema"
    }
  ]
}
```

验收标准：

- 每个 check 必须有独立实现类。
- 每个 check 必须可单元测试。
- LLM Judge prompt 必须版本化。
- Judge 输出必须结构化。

### 7.7 Replay

Replay 应支持三种模式：

| 模式 | 说明 |
| --- | --- |
| deterministic | 使用历史工具返回和固定模型参数重跑 |
| candidate | 使用新 prompt / 新模型 / 新代码重跑 |
| live | 使用真实工具重新查询 |

验收标准：

- replay 必须保留原始 task_id 和新的 run_id。
- replay 结果必须能与 baseline 比较。
- replay 过程中模型、prompt、代码版本必须记录。

### 7.8 Compare

Compare 用于比较 baseline 和 candidate。

比较维度：

- pass rate。
- 平均分。
- schema 通过率。
- 证据引用通过率。
- 工具调用成功率。
- 平均成本。
- 平均耗时。
- 退化任务列表。
- 改善任务列表。

报告示例：

```text
Baseline: run_001
Candidate: run_002

Pass Rate: 85% -> 90%
Avg Cost: $0.12 -> $0.09
Regression Cases: 2
Improved Cases: 5
Decision: PASS
```

验收标准：

- compare 结果必须输出 Markdown。
- 支持 `--fail-on-regression`。
- 支持成本和质量双阈值。

### 7.9 CI Gate

当以下文件发生变化时，CI 必须运行 eval subset：

```text
prompts/**
agent/**
tools/**
harness/**
rag/**
```

CI Gate 规则：

- pass rate 不低于 baseline 3%。
- 平均成本不能上涨超过 20%。
- forbidden_text 不能失败。
- schema 通过率必须 100%。
- 高优先级 task 不能退化。

验收标准：

- PR 中自动生成 eval report。
- CI 失败时输出退化 case 列表。
- 支持本地复现同一批 eval。

## 8. Agent Runtime 需求

### 8.1 Runtime 执行流程

```text
load task
-> create trace
-> classify
-> plan
-> policy check
-> tool execution
-> answer synthesis
-> eval
-> persist trace
-> return result
```

### 8.2 Runtime 约束

- 所有模型调用必须通过 Internal AI Client。
- 所有工具调用必须通过 Tool Hub。
- 所有步骤必须写入 trace。
- 工具权限必须由 Policy 检查。
- 超出 max_steps 必须停止。
- 超出 cost limit 必须停止。
- 高风险操作必须等待人工确认。

## 9. LiteLLM 需求

### 9.1 模型别名

系统应定义以下模型 profile：

| Profile | 用途 |
| --- | --- |
| fast | 分类、轻量摘要 |
| smart | 规划、复杂分析 |
| judge | Eval Judge |
| code | 代码理解和修复 |
| cheap | 批量低成本任务 |
| local | 本地模型实验 |

### 9.2 调用元数据

每次模型调用必须包含：

- trace_id。
- run_id。
- task_id。
- user_id。
- team_id。
- cost_center。
- prompt_version。
- model_profile。

验收标准：

- 业务代码不得直接调用模型供应商。
- 模型调用失败时支持 retry / fallback。
- LiteLLM 侧能统计用户、团队、任务维度成本。

## 10. RAG 需求

### 10.1 文档来源

MVP 阶段支持本地文件导入：

- Markdown 文档。
- Runbook。
- 历史工单 JSON。
- 服务说明文档。

### 10.2 检索流程

```text
document ingest
-> chunk
-> embedding
-> vector store
-> retrieve
-> rerank 可选
-> return citations
```

验收标准：

- 检索结果必须包含 source、title、chunk_id、score。
- AI 回答必须引用来源。
- Harness 可以 mock 检索结果。

## 11. Codex 课程需求

课程中需要展示 Codex 如何成为工程工作流的一部分。

### 11.1 必需 Codex 文件

```text
AGENTS.md
.codex/config.toml
skills/run-evals/
skills/debug-trace/
skills/fix-ticket/
skills/release-ai-change/
```

### 11.2 Codex Skill 需求

| Skill | 功能 |
| --- | --- |
| run-evals | 执行 harness eval 并总结失败项 |
| debug-trace | 读取失败 trace，定位 prompt/tool/code 问题 |
| fix-ticket | 根据代码型工单修改代码并运行测试 |
| release-ai-change | 发布前运行 eval、成本检查、安全检查 |

验收标准：

- 每个 skill 必须有清晰的输入、输出、命令和完成标准。
- Codex 修改 prompt、agent、tool 后必须运行相关 eval。
- Codex 生成 PR 描述时必须包含 eval 结果摘要。

## 12. 前端需求

MVP 前端需要 4 个页面。

### 12.1 Ticket Inbox

功能：

- 工单列表。
- 状态筛选。
- 优先级筛选。
- 创建工单。
- 触发 AI 分析。

### 12.2 Ticket Detail

功能：

- 工单原文。
- AI 处理状态。
- 分析结论。
- 证据列表。
- 推荐动作。
- 人工确认按钮。

### 12.3 Trace Viewer

功能：

- 展示 Agent 执行步骤。
- 展示模型调用。
- 展示工具调用。
- 展示 token、cost、latency。
- 展示最终输出和 eval 结果。

### 12.4 Eval Dashboard

功能：

- 展示 run 列表。
- 展示 pass rate。
- 展示成本变化。
- 展示退化 case。
- 展示 compare report。

## 13. 数据模型

核心表：

```text
users
teams
tickets
ticket_messages
agent_runs
trace_spans
model_calls
tool_calls
eval_tasks
eval_runs
eval_results
prompt_versions
documents
document_chunks
approval_requests
audit_logs
```

### 13.1 tickets

| 字段 | 类型 |
| --- | --- |
| id | uuid |
| title | text |
| description | text |
| category | text |
| priority | text |
| status | text |
| service | text |
| environment | text |
| created_by | uuid |
| created_at | timestamp |
| updated_at | timestamp |

### 13.2 agent_runs

| 字段 | 类型 |
| --- | --- |
| id | uuid |
| ticket_id | uuid |
| trace_id | text |
| task_id | text |
| status | text |
| model_profile | text |
| total_cost_usd | decimal |
| total_latency_ms | int |
| final_output | jsonb |
| created_at | timestamp |

### 13.3 trace_spans

| 字段 | 类型 |
| --- | --- |
| id | uuid |
| trace_id | text |
| parent_span_id | text |
| span_type | text |
| name | text |
| input | jsonb |
| output | jsonb |
| status | text |
| started_at | timestamp |
| ended_at | timestamp |

## 14. API 需求

### 14.1 工单 API

```http
POST /api/tickets
GET /api/tickets
GET /api/tickets/{id}
POST /api/tickets/{id}/run-agent
POST /api/tickets/{id}/approve
```

### 14.2 Trace API

```http
GET /api/traces/{trace_id}
GET /api/traces/{trace_id}/spans
GET /api/runs/{run_id}
```

### 14.3 Eval API

```http
GET /api/eval/tasks
POST /api/eval/runs
GET /api/eval/runs/{run_id}
POST /api/eval/compare
```

## 15. 非功能需求

### 15.1 性能

- 普通知识问答 15 秒内返回。
- 故障排查类任务 60 秒内返回初步结论。
- Harness 单机可运行 100 条 eval task。
- Trace 查询 P95 小于 1 秒。

### 15.2 安全

- 所有用户操作必须鉴权。
- 工具调用必须经过权限检查。
- 生产环境高风险动作必须人工确认。
- Prompt、Trace、Report 中不得泄露 secrets。
- 对外报告必须脱敏。

### 15.3 可观测性

- API、Agent、Tool、Harness、LiteLLM 都必须输出结构化日志。
- 关键链路必须接入 OpenTelemetry。
- 每个请求必须有 trace_id。
- 模型成本、token、latency 必须可统计。

### 15.4 可测试性

- Harness checkers 必须有单元测试。
- Tool mocks 必须可本地运行。
- Agent Runtime 必须支持 dry run。
- CI 必须能执行 eval subset。

## 16. 课程章节建议

课程可以拆成以下章节：

1. 项目介绍与企业级 AI 架构设计。
2. LiteLLM Proxy 搭建与模型别名设计。
3. Internal AI Client 和模型调用元数据。
4. 工单系统和 Agent Runtime 骨架。
5. Tool Hub 与 mock 工具实现。
6. RAG 文档导入、切分、向量检索和引用。
7. 手搓 Harness：Task Spec 与 Runner。
8. 手搓 Harness：Trace Schema 与 Span Recorder。
9. 手搓 Harness：Tool Mock 与 deterministic replay。
10. 手搓 Harness：Eval Checkers 与 LLM Judge。
11. 手搓 Harness：Baseline Compare 与 Regression Report。
12. Harness 接入 CI Gate。
13. Codex AGENTS.md、skills、debug-trace 工作流。
14. Codex 辅助修复代码型工单。
15. 前端 Trace Viewer 与 Eval Dashboard。
16. 权限、审计、预算、成本治理。
17. 课程总结：从 demo 到企业落地。

## 17. 交付物

课程最终应交付：

1. 可运行项目代码。
2. Docker Compose 本地环境。
3. LiteLLM 配置。
4. 20 条以上 golden tasks。
5. 10 条以上 mock tool fixtures。
6. Harness CLI。
7. Eval report 示例。
8. Trace viewer 页面。
9. Codex skills。
10. CI workflow。
11. 项目架构文档。
12. 课程讲义和练习题。

## 18. 验收标准

项目最终验收时应满足：

1. 用户可以创建工单并触发 AI 分析。
2. Agent 可以完成分类、规划、工具调用和结构化输出。
3. LiteLLM 能统一代理模型请求。
4. 每次 AI 任务都有完整 trace。
5. Harness 可以运行至少 20 条任务。
6. Harness 可以 replay 历史任务。
7. Harness 可以比较 baseline 和 candidate。
8. CI 可以基于 eval 结果失败。
9. Trace Viewer 可以展示模型调用、工具调用、成本和耗时。
10. Codex 可以通过 skill 运行 eval 并调试失败 trace。

## 19. 优先级建议

### P0

- LiteLLM Proxy。
- Internal AI Client。
- Agent Runtime 最小闭环。
- Harness Task Runner。
- Trace Recorder。
- Tool Mock。
- Eval Checkers。
- 20 条 Golden Tasks。

### P1

- Replay。
- Compare。
- CI Gate。
- RAG。
- Trace Viewer。
- Eval Dashboard。
- Codex Skills。

### P2

- MCP 接入真实企业系统。
- 多租户预算。
- 人工审批。
- Langfuse/OpenTelemetry 深度集成。
- 自动 PR 修复流程。

## 20. 设计原则

1. 所有 AI 行为必须可观测。
2. 所有重要 AI 行为必须可回放。
3. 所有上线前 AI 改动必须可评测。
4. 模型供应商不能侵入业务代码。
5. 工具调用必须有权限边界。
6. 课程重点放在工程能力，而不是 prompt 炫技。
7. Harness 是核心学习对象，必须手搓关键路径。
8. Codex 是工程协作者，不是生产运行时。
