# 企业级 AI 工程实战课程大纲

## 课程名称

**企业级 AI 工程实战：LiteLLM、Codex 与自研 Harness**

副标题：

**从零构建可评测、可回放、可治理的 AI 工单平台**

## 课程定位

本课程面向有较多开发经验的工程师，不以普通 Chatbot 为目标，而是围绕一个企业内部 AI 工单与故障处理平台，完整讲解 AI 应用工程化落地。

课程主线：

```text
搭建 LiteLLM + Codex 本地 AI 开发环境
-> 实现工单系统与 Agent Runtime
-> 接入 Tool Hub 与 Mock 工具
-> 跑通第一个端到端 AI 工单案例
-> 手搓 AI Harness
-> 实现 Trace / Eval / Replay / Compare / CI Gate
-> 使用 Codex 固化工程工作流
```

课程重点不是“调 prompt”，而是让学习者掌握：

1. 如何搭建企业级 AI 应用工程骨架。
2. 如何通过 LiteLLM 管理多模型调用。
3. 如何把 Codex 融入本地开发工作流。
4. 如何手搓 AI Harness，让 AI 行为可评测、可回放、可回归。
5. 如何把 AI 改动纳入 CI/CD 和工程治理。

## 课程总结构

| 课时 | 主题 | 重点 |
| --- | --- | --- |
| 第 1 课 | 搭建 LiteLLM + Codex 本地 AI 开发环境 | 本地 AI 工程底座、LiteLLM、Codex、AI Client |
| 第 2 课 | 工单系统与 Agent Runtime 骨架 | 工单 API、Agent 执行流、结构化输出 |
| 第 3 课 | Tool Hub、Mock 工具与 Policy | 工具调用、Mock Fixtures、权限和风险控制 |
| 第 4 课 | 跑通第一个端到端 AI 工单案例 | 工单 -> Agent -> 工具 -> 模型 -> 结果 |
| 第 5 课 | 手搓 Harness：Task Spec 与 Runner | YAML Task、CLI Runner、任务执行 |
| 第 6 课 | 手搓 Harness：Trace Recorder | Trace Schema、Span、成本和耗时记录 |
| 第 7 课 | 手搓 Harness：Eval Checkers 与 LLM Judge | 规则评测、Judge、结构化评分 |
| 第 8 课 | 手搓 Harness：Tool Mock 与 Deterministic Replay | 工具 Mock、历史返回复用、确定性回放 |
| 第 9 课 | 手搓 Harness：Compare、Regression Report 与 CI Gate | Baseline 比较、退化报告、CI 门禁 |
| 第 10 课 | Codex Skills、失败 Trace 调试与完整项目演示 | Codex 工作流、debug trace、最终演示 |

建议每节课控制在 **35-50 分钟**。

每节课推荐节奏：

```text
5 分钟：这一课要解决什么问题
10 分钟：架构和关键设计讲解
25-30 分钟：编码实现
5 分钟：运行演示和本课总结
```

## 第 1 课：搭建 LiteLLM + Codex 本地 AI 开发环境

### 本课目标

第一节课结束时，学习者应该拥有一个可以本地开发的 AI 工程环境：

```text
LiteLLM Proxy
+ Postgres
+ Redis
+ Codex 项目配置
+ Internal AI Client
+ 第一次模型调用
```

### 讲解内容

1. 课程项目介绍。
2. 为什么需要 LiteLLM。
3. 为什么需要 Codex。
4. 为什么后面要手搓 Harness。
5. 初始化 monorepo。
6. 使用 Docker Compose 启动 Postgres、Redis、LiteLLM Proxy。
7. 配置 LiteLLM 模型别名。
8. 配置 Codex 项目规则。
9. 实现 Internal AI Client v0。
10. 编写 smoke test 验证模型调用。

### 推荐项目结构

```text
apps/
  api/
  web/
packages/
  ai-client/
  harness/
  agent-runtime/
  tool-hub/
  rag/
infra/
  litellm/
docs/
prompts/
tasks/
scripts/
```

### LiteLLM 模型别名

```text
fast    -> 轻量分类、摘要
smart   -> 复杂分析、规划
judge   -> eval judge
code    -> 代码理解和修复
cheap   -> 批量低成本任务
```

### Codex 项目配置

第一课只需要让 Codex 理解项目的基本规则、命令和目录结构。

推荐创建：

```text
AGENTS.md
.codex/config.toml
```

第一课暂时不实现 Codex skills，skills 放到第 10 课集中讲。

### Internal AI Client v0

需要实现：

```text
generate()
generate_json()
judge()
```

每次请求必须携带：

```text
trace_id
run_id
task_id
model_profile
prompt_version
cost_center
```

### 本课交付物

```text
infra/docker-compose.yml
infra/litellm/config.yaml
packages/ai-client/
AGENTS.md
.codex/config.toml
scripts/smoke_ai_client.py
```

### 本课验收

运行：

```bash
python scripts/smoke_ai_client.py
```

期望输出类似：

```text
LiteLLM connected
model_profile=fast
response ok
trace_id generated
```

## 第 2 课：工单系统与 Agent Runtime 骨架

### 本课目标

实现最小工单系统，并让工单可以触发 Agent Runtime。

### 讲解内容

1. 工单领域模型设计。
2. 工单状态机。
3. API 设计。
4. Agent Runtime 基础执行流。
5. 分类、规划、答案生成。
6. 结构化输出。

### 需要实现的 API

```http
POST /api/tickets
GET /api/tickets
GET /api/tickets/{id}
POST /api/tickets/{id}/run-agent
```

### Agent Runtime v0 执行流

```text
load ticket
-> classify
-> plan
-> synthesize answer
-> return structured result
```

### 本课交付物

```text
apps/api/
packages/agent-runtime/
database tickets table
prompts/classify_ticket.md
prompts/plan_ticket.md
prompts/synthesize_answer.md
```

### 本课验收

1. 可以创建工单。
2. 可以触发 AI 分析。
3. Agent 可以返回结构化结果。
4. 模型调用全部通过 Internal AI Client。

## 第 3 课：Tool Hub、Mock 工具与 Policy

### 本课目标

实现集中式 Tool Hub，并先用 Mock 工具模拟企业内部系统。

### 讲解内容

1. 为什么工具调用需要集中管理。
2. 工具 allowlist。
3. Mock Fixtures 设计。
4. 工具输入输出 schema。
5. Policy Check。
6. 高风险工具调用识别。

### MVP 工具列表

```text
search_docs
search_runbook
search_tickets
query_logs
query_metrics
search_code
get_ci_status
```

### 本课交付物

```text
packages/tool-hub/
fixtures/tools/
packages/agent-runtime/policy/
```

### 本课验收

1. Agent 可以调用 Tool Hub。
2. 工具返回来自 fixture。
3. 工具调用经过 allowlist 检查。
4. 工具调用失败时 Agent 可以降级处理。

## 第 4 课：跑通第一个端到端 AI 工单案例

### 本课目标

用一个真实风格案例跑通完整业务链路。

案例：

```text
登录服务 500 错误增多
```

完整链路：

```text
用户提交工单
-> Agent 分类
-> Agent 规划
-> 查询 Runbook
-> 查询日志
-> 查询监控
-> 搜索代码
-> 生成结构化分析结果
```

### 结构化输出示例

```json
{
  "summary": "登录服务 500 错误主要集中在 auth-service 的 token 校验路径",
  "suspected_root_cause": "新版本引入的空指针异常",
  "evidence": [
    "日志显示 TokenParser.parse 出现 NullPointerException",
    "监控显示 10:05 后错误率上升",
    "CI 记录显示 auth-service 在 10:00 完成发布"
  ],
  "recommended_actions": [
    "回滚 auth-service 到上一稳定版本",
    "检查 TokenParser 的 null handling"
  ],
  "confidence": 0.82,
  "risk_level": "medium"
}
```

### 本课交付物

```text
demo ticket fixture
end-to-end agent flow
structured incident result
```

### 本课验收

1. 能通过 API 创建案例工单。
2. 能触发 Agent 分析。
3. 能看到工具调用结果。
4. 能得到结构化故障分析。

## 第 5 课：手搓 Harness：Task Spec 与 Runner

### 本课目标

从这一课开始进入课程核心：手搓 AI Harness。

本课实现 Task Spec 和 CLI Runner，让 AI 任务可以脱离前端和 API，从命令行稳定运行。

### 讲解内容

1. Harness 为什么是企业 AI 工程底座。
2. Task Spec 设计。
3. YAML 配置校验。
4. CLI 设计。
5. Runner 如何调用 Agent Runtime。
6. limits、allowed tools、expected、eval 配置。

### Task Spec 示例

```yaml
id: incident-login-500
name: 登录服务 500 错误排查
type: incident_triage
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
eval:
  checks:
    - schema
    - required_fields
    - tool_usage
    - cost_limit
```

### CLI 命令

```bash
ai-harness run tasks/incident-login-500.yaml
ai-harness run tasks/ --model smart --limit 20
```

### 本课交付物

```text
packages/harness/
tasks/incident-login-500.yaml
ai-harness run
```

### 本课验收

1. Task Spec 可以被校验。
2. 缺少关键字段时有友好错误。
3. CLI 可以运行单个 task。
4. limits 能传递给 Agent Runtime。

## 第 6 课：手搓 Harness：Trace Recorder

### 本课目标

为每次 AI 任务记录完整 trace，让模型调用、工具调用、Agent 步骤和评测结果可观察。

### 讲解内容

1. Trace 和普通日志的区别。
2. Trace Schema 设计。
3. Span 设计。
4. token、cost、latency 记录。
5. prompt hash 和 tool output hash。
6. 敏感信息脱敏。

### Span 类型

```text
agent.step
model.call
tool.call
rag.retrieve
policy.check
eval.check
```

### Trace 核心字段

```json
{
  "trace_id": "trace_001",
  "task_id": "incident-login-500",
  "run_id": "run_001",
  "model_profile": "smart",
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

### 本课交付物

```text
packages/harness/trace/
traces/run-001.json
ai-harness inspect
```

### 本课验收

1. 每次任务运行都会生成 trace。
2. model.call span 记录模型、token、cost。
3. tool.call span 记录工具名称、输入输出 hash、耗时。
4. 可以用 CLI 查看 trace 摘要。

## 第 7 课：手搓 Harness：Eval Checkers 与 LLM Judge

### 本课目标

实现可组合的评测器，让 AI 输出可以被自动判定质量。

### 讲解内容

1. 规则评测 vs LLM Judge。
2. Checker 抽象设计。
3. schema check。
4. required_fields check。
5. forbidden_text check。
6. tool_usage check。
7. evidence_citation check。
8. cost_limit / latency_limit check。
9. LLM Judge prompt 版本化。

### 推荐 Checkers

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

### Eval Result 示例

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

### 本课交付物

```text
packages/harness/checkers/
prompts/judge_factuality.md
prompts/judge_helpfulness.md
```

### 本课验收

1. 每个 checker 可以单独测试。
2. Harness run 可以执行 eval checks。
3. LLM Judge 输出结构化评分。
4. Eval 结果进入 trace。

## 第 8 课：手搓 Harness：Tool Mock 与 Deterministic Replay

### 本课目标

实现工具 mock 和确定性回放，让历史 AI 任务可以稳定复现。

### 讲解内容

1. 为什么 replay 必须 mock 工具。
2. 历史工具返回复用。
3. Mock Fixture 匹配。
4. deterministic replay。
5. candidate replay。
6. live replay。
7. 回放结果如何进入新的 run。

### Mock 示例

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

### CLI 命令

```bash
ai-harness replay traces/run-001.json
ai-harness run tasks/incident-login-500.yaml --mock-tools
```

### 本课交付物

```text
packages/harness/mock/
fixtures/tool-mocks/
ai-harness replay
```

### 本课验收

1. replay 可以使用历史工具返回。
2. task run 可以使用 mock fixture。
3. mock 未命中时有明确错误。
4. replay 生成新的 run_id。

## 第 9 课：手搓 Harness：Compare、Regression Report 与 CI Gate

### 本课目标

实现 baseline 和 candidate 对比，并把 eval 接入 CI，让 AI 改动也有回归门禁。

### 讲解内容

1. baseline / candidate 的概念。
2. pass rate 比较。
3. 平均分、成本、耗时比较。
4. regression cases。
5. improved cases。
6. Markdown/HTML report。
7. GitHub Actions 接入。
8. 质量阈值和成本阈值。

### Compare 输出示例

```text
Baseline: run_001
Candidate: run_002

Pass Rate: 85% -> 90%
Avg Cost: $0.12 -> $0.09
Regression Cases: 2
Improved Cases: 5
Decision: PASS
```

### CI Gate 规则

```text
schema 通过率必须 100%
pass rate 不能低于 baseline 3%
平均成本不能上涨超过 20%
高优先级 task 不能退化
forbidden_text 不能失败
```

### 本课交付物

```text
ai-harness compare
ai-harness report
.github/workflows/eval.yml
reports/eval-report.md
```

### 本课验收

1. 可以比较两组 runs。
2. 可以输出退化任务列表。
3. 支持 `--fail-on-regression`。
4. CI 可以基于 eval 结果失败。

## 第 10 课：Codex Skills、失败 Trace 调试与完整项目演示

### 本课目标

把 Codex 融入工程工作流，并完成课程最终演示。

### 讲解内容

1. Codex 在项目中的定位。
2. 如何写 AGENTS.md。
3. 如何配置项目级 Codex。
4. 如何把重复动作做成 skill。
5. 用 Codex 跑 eval。
6. 用 Codex 分析失败 trace。
7. 用 Codex 修改代码或 prompt。
8. 重新运行 harness compare。
9. 最终完整项目演示。

### 推荐 Skills

```text
skills/run-evals/
skills/debug-trace/
skills/fix-ticket/
skills/release-ai-change/
```

### Skill 职责

| Skill | 功能 |
| --- | --- |
| run-evals | 执行 harness eval 并总结失败项 |
| debug-trace | 读取失败 trace，定位 prompt/tool/code 问题 |
| fix-ticket | 根据代码型工单修改代码并运行测试 |
| release-ai-change | 发布前运行 eval、成本检查、安全检查 |

### 最终演示链路

```text
创建工单
-> Agent 处理
-> 查看 Trace
-> 修改 Prompt
-> Harness Replay
-> Compare Baseline / Candidate
-> CI Gate
-> Codex Debug Trace
-> 修复问题
-> 再次通过 Eval
```

### 本课交付物

```text
AGENTS.md
.codex/config.toml
skills/run-evals/
skills/debug-trace/
skills/fix-ticket/
skills/release-ai-change/
final demo script
```

### 本课验收

1. Codex 可以按项目规则运行。
2. Codex 可以触发 Harness eval。
3. Codex 可以分析失败 trace。
4. Codex 可以辅助修复问题。
5. 最终项目可以完整演示。

## 课时重点分配

建议权重：

```text
AI 应用基础：第 1-4 课，占 40%
手搓 Harness：第 5-9 课，占 50%
Codex 工程流：第 10 课，占 10%
```

这门课的核心卖点应该放在：

1. 从 0 手搓 AI Harness。
2. 让 Agent 行为可复现。
3. 让 Prompt / Model / Tool 改动可回归测试。
4. 用 LiteLLM 管住模型调用。
5. 用 Codex 固化工程工作流。

## 最终交付物

课程完成后，学习者应得到：

```text
可运行项目代码
LiteLLM 本地模型网关
Internal AI Client
工单系统 API
Agent Runtime
Tool Hub 与 Mock 工具
AI Harness CLI
Trace Recorder
Eval Checkers
LLM Judge
Replay
Compare
CI Gate
Codex Skills
完整演示案例
```
