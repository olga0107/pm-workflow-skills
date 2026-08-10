---
name: pm-requirement-grade
description: 对产品需求进行通用风险分级和交付路由。Use when Codex needs to classify a requirement as L0/L1/L2/L3/H, decide whether product/business self-service AI Coding or VibeCoding is allowed, identify red-line risks, and output the matching routing/gate pack: L0 change record, L1 AI Coding task brief, L2 collaboration brief, L3 PRD/spec review gate, or H hotfix governance pack. This skill does not replace pm-requirement-define, pm-prd-write, engineering specs, QA plans, or metrics review. Also use for 兴趣岛/XQD/xqd-learning-weapp mini-program demand grading with project-specific red lines.
---

# pm-requirement-grade

负责在需求分析之后完成两件事：**风险分级**和**交付路由 / 门禁包**。它是需求分析之后、PRD/研发/测试交付之前的统一路由入口，不是 PRD、研发 spec、测试方案或指标复盘的替代品。

## 优先读取

1. [通用需求风险分级矩阵](./references/risk-matrix.md)：L0/L1/L2/L3/H 定义、红线和流程路由。
2. [需求分级卡](./templates/需求分级卡.md)：需要沉淀评级输入、补齐待确认项或留档时使用；它不是需求定义模板。
3. [分级评审输出模板](./templates/分级评审输出模板.md)：输出标准化评级结论和下一步路由时使用。
4. [xqd-learning-weapp 项目画像](./references/project-profile-xqd-learning-weapp.md)：仅当上下文涉及兴趣岛/XQD、`xqd-learning-weapp`、小程序、课程、直播、回放、支付或权益时读取；项目红线只用于升档和门禁，不替代项目 PRD。
5. [L3 高风险需求评审清单](./templates/L3评审清单.md)：仅在输出或检查 L3 评审门禁时使用；它不是 PRD 模板，PRD 内容标准以 `pm-prd-write` 为准。

## 工作边界

本 skill 回答：

- 当前需求分析是否足以评级；不足时应回到哪个上游 skill。
- 建议等级是 L0/L1/L2/L3/H 中哪一类。
- 产品/业务方 AI Coding 自助是否允许，以及允许条件。
- 是否需要 PRD、研发 spec、评审、QA、灰度、回滚和上线观察。
- 按等级输出**交付路由包 / 门禁包**：L0 变更记录、L1 AI Coding 任务边界、L2 协作简报、L3 PRD/spec 评审门禁、H hotfix 治理包。

本 skill 不回答：

- 不重新发散需求方向和方案取舍；需求分析不足时回到 `pm-requirement-define`。
- 不编写完整 PRD，也不定义 PRD 章节标准；L3 或复杂 L2 需要完整 PRD 时，只输出 `pm-prd-write` 的输入摘要、风险门槛和 PRD 需覆盖的重点。
- 不替研发写接口字段、存储、队列、算法和代码实现；只指出是否需要研发 spec、哪些风险必须在 spec 中被处理。
- 不替测试编写完整测试方案；只指出 QA 覆盖范围和必须评审的风险类型。
- 不用上线观察记录替代 `pm-metrics-review`；上线后需要判断效果、异常原因或继续 / 回滚决策时交给 `pm-metrics-review`。

## 与下游产物的边界

`pm-requirement-grade` 的模板只回答“当前风险等级要求哪些下游产物齐备”，不回答“这些下游产物应该完整写成什么样”。

| 下游内容 | 本 skill 只输出 | 正式标准 / 下游 owner |
|---|---|---|
| 需求定义 | 评级所需完整性缺口和退回原因 | `pm-requirement-define` |
| PRD | 是否需要 PRD、PRD 必填风险重点、交给 PRD 的输入摘要 | `pm-prd-write` 及其 PRD 模板 |
| 研发 spec | 是否需要 spec、必须处理的技术风险主题 | 研发 / 技术方案，不在本 skill 写接口字段和实现方案 |
| 测试方案 | 必须覆盖的风险类型和验收门槛 | QA / 测试方案，不在本 skill 展开完整用例集 |
| 上线观察 | 观察项、周期、责任人和暂停 / 回滚信号 | `pm-metrics-review` 负责效果复盘、异常诊断和因果判断 |
| 更新同步 | 是否需要同步及受众 | `pm-update-write` 负责正式更新说明 / 通知 / 日志 |

如果模板中的“简版需求说明”“评审清单”“上线观察记录”开始需要承载完整规则、状态矩阵、指标口径或跨团队正式口径，应停止在本 skill 内扩写，并转给对应下游 skill。

## 分级流程

1. **检查需求分析完整性**：确认用户、问题、目标、范围、非目标、入口/页面/模块、数据读写、上线场景、验收和回滚。若缺口会改变等级，不得默认 L1。
2. **识别项目画像**：如果用户给出仓库、业务线或平台，读取对应项目规则；没有项目画像时使用通用矩阵并标注未知项。
3. **扫描红线**：资金/交易、身份/权限/隐私、权益/资产、核心链路、数据写入/状态机、AI 自动化结果、外部依赖、全局配置、生产数据、不可快速回滚、线上故障。
4. **按最高风险定级**：任何 L3 红线命中即 L3；线上故障止血为 H；不因代码量小、页面少或 AI 能实现而降级。
5. **输出标准化路由包**：按最终等级输出固定结构；同一次输出中必须先给评级结论，再给门禁要求和下一步交接，不在本 skill 内扩写下游正式产物。

## 等级定义与交付路由

| 等级 | 定义 | 本 skill 输出 |
|---|---|---|
| L0 | 内容、文案、配置或文档级变更；不改业务逻辑、不改路径、不改权限、不写数据、不影响核心体验 | L0 变更记录 |
| L1 | 独立、非核心、范围清楚、无红线、可构建、可完整自测、可快速回滚 | L1 AI Coding 任务边界 + 上线门禁 |
| L2 | 影响已有页面、共享组件、已有接口展示或历史路径，风险可控且不触及 L3 红线 | L2 协作简报 + 影响面 / spec / QA 路由 |
| L3 | 涉及资金、权益、身份、隐私、生产数据写入、状态机、核心链路、全局配置、外部依赖、AI 自动化结果沉淀或不可快速回滚 | L3 PRD/spec 评审门禁 + 下游交接摘要 |
| H | 线上已发生或正在发生的问题，需要快速止血 | H hotfix 治理包 + 复盘 / 长期修复路由 |

## 默认输出结构

```markdown
# 需求分级与交付路由

## 1. 分级结论
- 建议等级：L0 / L1 / L2 / L3 / H
- AI Coding 自助：允许 / 有条件允许 / 不允许
- 主要原因：
- 本次路由包：L0 变更记录 / L1 AI Coding 任务边界 / L2 协作简报 / L3 PRD-spec 评审门禁 / H hotfix 治理包
- 对应下一步 skill：pm-requirement-define / pm-prd-write / 暂不需要

## 2. 需求分析完整性
| 项目 | 结论 | 说明 |
|---|---|---|
| 用户与问题 | 已清楚/待补 |  |
| 目标与成功标准 | 已清楚/待补 |  |
| 范围与非目标 | 已清楚/待补 |  |
| 入口/页面/模块 | 已清楚/待补 |  |
| 数据读写与权限 | 已清楚/待补 |  |
| 验收与回滚 | 已清楚/待补 |  |

## 3. 风险命中依据
| 检查项 | 结果 | 说明 |
|---|---|---|
| 资金/订单/支付/价格 | 未命中/命中/待确认 |  |
| 登录/授权/隐私/token | 未命中/命中/待确认 |  |
| 权益/资产/核心链路 | 未命中/命中/待确认 |  |
| AI 自动化结果/长期资产 | 未命中/命中/待确认 |  |
| 后端写入/状态机/生产数据 | 未命中/命中/待确认 |  |
| 全局配置/外部依赖/基础设施 | 未命中/命中/待确认 |  |
| 可自测/可回滚 | 是/否/待确认 |  |
| 项目画像红线 | 未命中/命中/不适用 |  |

## 4. 交付路由包
- 路由包类型：
- 门禁要求：
- 交给下游的输入摘要：
- 不能在本 skill 内展开的事项：
- 相关模板/文档：

## 5. 下一步
- 需要补充的信息：
- 是否需要 PRD：不需要 / L2 协作简报 / 完整 PRD
- 是否需要研发 spec：不需要 / 按需 / 必须
- 是否需要评审 / QA / 灰度 / 回滚：
- 对应下一步 skill：pm-requirement-define / pm-prd-write / 暂不需要
```

## 完成标准

- 明确给出 `建议等级`、`AI Coding 自助` 和对应交付路由 / 门禁。
- 对每个可能升档的关键风险给出命中、未命中或待确认状态。
- 信息不足时只问会改变等级或流程的关键问题，并明确建议回到 `pm-requirement-define` 的原因。
- L1 必须输出 AI Coding 任务边界和最小门禁；L2/L3/H 必须说明为什么不能按 L1 处理。
- L2 简版说明不得升级成事实上的完整 PRD；复杂 L2 转 `pm-prd-write`。
- L3 必须输出 PRD 必填风险重点和研发 spec 评审主题，但不替 `pm-prd-write` 写 PRD，也不替研发写实现细节。
- 上线观察只记录监测和动作，不做效果因果判断；需要复盘时转 `pm-metrics-review`。
- 若涉及项目画像，必须说明是否命中项目专属红线。
