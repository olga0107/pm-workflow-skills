# PROGRESS

- 目标：完成整套 PM Workflow Skills 的收尾审计与维护，尤其把后续单点加入的 `pm-requirement-grade` 串回完整工作流，统一仓库级引导、上下游交接和维护规范。
- 当前工作流：证据补齐（按需）→ `pm-requirement-define` → `pm-requirement-grade` → L0/L1/L2/L3/H 对应交付 → `pm-prd-write` / `pm-update-write` / `pm-metrics-review` 闭环。
- 本轮判断：原有 README 与 WORKFLOW_GUIDE 已能提到分级，但对“何时用、怎么串、上下游交接契约、理想协作实践”的说明不足；`pm-requirement-define` 和 `pm-prd-write` 中也仍有少量“直接进 PRD”的旧口径，需要统一为先分级再交付。

## 本轮完成

- 重写 `README.md`，从仓库入口层面说明完整主线、7 个 skills 的职责、分级门禁和 XQD 兼容规则。
- 重写 `WORKFLOW_GUIDE.md`，补齐总体流程图、skill 职责地图、输入成熟度判断、C1-C5 上下游交接契约、L1/L2/L3/H 理想实践和统一规范。
- 更新 `pm-requirement-define`，将输出定位从“可写 PRD”调整为“可进入需求分级与后续交付路由”，并补充交给 `pm-requirement-grade` 的风险线索契约。
- 更新 `pm-prd-write`，显式接收 `pm-requirement-grade` 的分级结论、AI Coding / 协作 / PRD 门槛、spec / QA / 灰度 / 回滚 / 上线观察要求。
- 更新 `commands/pm-requirement-define.md`、`CONTRIBUTING.md`、`ITERATION_GUIDE.md`、`CHANGELOG.md` 和上游映射，统一“需求定义后先分级”的口径。


## 二次收敛审查

- 结论：核心调整必要；本轮不是新增复杂度，README 从旧版 232 行收敛到 44 行，WORKFLOW_GUIDE 从旧版 277 行收敛到 185 行。
- 已收敛：回退 PR 模板变更；删除 WORKFLOW_GUIDE 中与 PRD / CONTRIBUTING 重复的 ID 追溯和维护检查清单细节，只保留主线、交接契约和等级实践。
- 保留理由：需求分级是新增门禁，必须同步 README、WORKFLOW_GUIDE、`pm-requirement-define`、`pm-prd-write`、命令入口、模板和迭代指南，否则会继续出现“需求定义 ready 后直接写 PRD”的旧口径。


## pm-requirement-grade 边界审查

- 结论：存在单点并入后的边界混淆风险，尤其是 L2 简版、L3 评审清单和上线观察记录容易被误解为 PRD / spec / 测试 / 指标复盘标准。
- 已处理：将 `pm-requirement-grade` 明确收敛为“风险分级 + 交付路由 / 门禁包”，新增下游边界表；所有 grade 私有模板和 references 增加定位说明。
- 保留原则：grade 可以判断“是否需要 PRD/spec/QA/观察”和“门禁重点”，但不能在本 skill 内展开完整 PRD、研发实现、测试用例集或效果因果复盘。

## 验证记录

- `bash scripts/validate-skills.sh`：通过，8 个 skill。
- `python3 scripts/validate-docs.py`：通过，49 个 Markdown 文件、链接、表格和工作流约定。
- `git diff --check`：通过。

## 本轮页面体验工作流升级（2026-08-20）

- 结论：复杂页面需求不能只依赖页面地图、组件骨架和代表性原型；当目标是设计前评估页面效果时，必须增加页面内容契约，维护所有用户可见静态 / 动态 / 条件 / 反馈内容。
- 新增共享参考 `shared-references/页面内容契约与UX原型.md`，统一信息架构、页面内容契约、状态组合矩阵和 UX 原型的职责边界。
- 同步更新需求定义、需求分级、PRD 编写、HTML 编译及仓库级交接 / 迭代文档，形成需求定义 → 分级门槛 → PRD 内容主源 → HTML 内容覆盖的完整链路。
- 已完成：运行仓库校验；待完成：提交并推送远程、同步 Codex 本地 skills，再用真实页面需求回归。
