# PM Workflow Skills

面向 Codex 的产品工作流 skills 集合。它不是一组彼此独立的写作模板，而是一条从“模糊提需 / 证据材料”到“分级治理 / 交付规格 / 上线复盘”的可衔接工作流。

核心顺序：**需求定义 / 决策充分性判断 → 证据补齐（按需并回流） → 需求分级与交付路由 → PRD / 协作交付 / AI Coding 任务边界 → 更新同步 → 指标复盘与迭代**。

## Skills 一览

| Skill | 何时使用 | 输出交给谁 |
|---|---|---|
| `pm-requirement-define` | 想法、口头提需、问题、方向或一级范围尚未确认 | 交给 `pm-requirement-grade` 做等级和交付路由 |
| `pm-requirement-grade` | 需求定义基本完成，需要判断 L0/L1/L2/L3/H、AI Coding 是否允许、交付门槛是什么 | 交给 AI Coding、协作评审、`pm-prd-write` 或 hotfix 流程 |
| `pm-prd-write` | 已确认问题、目标、方向、一级范围和分级结论，需要展开可评审、可实现、可验收的 PRD | 交给设计、研发 spec、测试、发布与 `pm-update-write` |
| `pm-research-synthesize` | 有访谈、问卷、客服、可用性测试或开放文本，需要提炼用户证据 | 交回 `pm-requirement-define`，不直接替代产品决策 |
| `pm-competitor-analyze` | 需要比较外部解法、竞品机制或替代方案来支持决策 | 交回 `pm-requirement-define`，不直接把竞品做法当需求 |
| `pm-metrics-review` | 需要复盘目标、上线效果、异常波动或补充规模 / 效果证据 | 行动可交给 `pm-requirement-define`、`pm-update-write` 或后续交付流程 |
| `pm-update-write` | 结论、范围、上线内容或计划变化已经确认，需要同步、通知或留档 | 交给目标受众执行；后续效果进入 `pm-metrics-review` |

## 推荐工作流

1. **先判断输入成熟度**：模糊想法、口头提需或未定方向先用 `pm-requirement-define` 判断是否足以决策；证据缺口会影响判断时，再按需使用研究、竞品或指标 skill 并回流到需求定义。
2. **需求定义只做产品决策**：确认为什么做、做什么方向、做到哪里、不做什么、有哪些重大约束和成功假设。
3. **统一进入分级门禁**：用 `pm-requirement-grade` 判断 L0/L1/L2/L3/H；不因“改动小”“AI 能写”跳过资金、权益、登录、隐私、生产数据、状态机、核心链路、外部依赖等红线。
4. **按等级选择交付**：
   - L0 → 变更记录即可。
   - L1 → AI Coding 任务边界、自测、上线前检查和回滚说明。
   - L2 → 协作简报、研发影响面评估、QA 和上线观察。
   - L3 → 完整 PRD、研发 spec、测试方案、灰度 / 回滚 / 监控和评审治理。
   - H → hotfix 治理包，先止血，再补测试、复盘和长期修复。
5. **PRD 只在需要时展开**：`pm-prd-write` 接收需求定义和分级结论，负责页面、流程、规则、状态、权限、验收和 PRD/spec 边界；不重新做方向选择。
6. **更新与复盘闭环**：已确认变化用 `pm-update-write` 同步；上线效果、目标复盘或异常诊断用 `pm-metrics-review`，必要时回到需求定义重新决策。

完整用法、交接契约和理想实践见 [WORKFLOW_GUIDE.md](./WORKFLOW_GUIDE.md)。贡献、命名和校验规范见 [CONTRIBUTING.md](./CONTRIBUTING.md)。真实反馈如何沉淀见 [ITERATION_GUIDE.md](./ITERATION_GUIDE.md)。

## 上下游交接原则

- 每个阶段输出都必须说明：已确认事实、分析推断、待确认项、负责人 / 最晚时间、下一步 skill 或交付角色。
- 上游可以为下游提供摘要，但不能替下游展开职责；下游可以复述上游结论，但不能悄悄改变上游决策。
- 分级是需求定义之后、交付之前的统一门禁；L1 自助、L2 协作、L3 PRD/spec、H hotfix 都以分级结论为入口。
- 项目画像、项目仓库规则和业务红线优先于通用降级判断。

## 原项目兼容

识别到兴趣岛/XQD、`xqd-learning-weapp`、小程序、课程、直播、回放、支付或权益时，必须叠加 `pm-requirement-grade` 的项目画像和红线，不得因为通用化而放松原项目门槛。
