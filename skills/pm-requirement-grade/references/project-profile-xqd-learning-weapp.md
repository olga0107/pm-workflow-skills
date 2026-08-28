# 项目画像：xqd-learning-weapp / 兴趣岛小程序

> 定位：本画像只提供 xqd-learning-weapp 的**项目红线和升档规则**。它不定义项目需求、PRD 或研发实现标准；具体事实仍以项目仓库和已确认文档为准。

适用仓库：`/Users/huangjingye/Documents/project/xqd-learning-weapp`

当需求上下文出现“兴趣岛”“XQD”“xqd-learning-weapp”“小程序”“课程”“学习”“直播”“回放”“支付”“权益”等关键词，或用户明确在该仓库工作时，必须叠加本项目画像。通用化不弱化本项目红线。

## 默认 L3：禁止产品自助改完直接上线

- `src/apis/order.ts`
- `src/utils/pay.ts`
- `src/utils/safePay.ts`
- `src/utils/weappPay.ts`
- `src/utils/http.ts`
- `src/utils/encrypt.ts`
- `src/store/login`
- `src/new-live`
- `src/new-live-v2`
- `src/components/tencent-video-player`
- `src/components/player-control`
- `src/app.config.ts`
- `src/app.tsx`
- `src/pages/web-view`

## 默认至少 L2：需协作评审

- `src/pages/learn-list`
- `src/pages/course-detail`
- `src/pages/study-list`
- `src/components` 下被多页面复用的组件
- 埋点、监控、列表分页、筛选、排序等体验和数据行为
- 使用已有接口但改变展示、排序、过滤、状态解释或异常处理的需求

## L1 候选范围

- 新建独立静态说明页。
- 非核心页面样式、文案、空态、加载态调整。
- 私有组件且仅被当前页面使用。
- 不改变接口参数、状态判断、权限判断、权益判断、学习进度判断。
- PRD、设计文档、运营说明文档。

## 原项目流程保留

- L1：在 `pm-requirement-grade` 内输出 AI Coding 任务边界和门禁，限定文件白名单，执行 `npm run build:weapp`，微信开发者工具自测，保留截图/录屏和回滚方案。
- L2：在 `pm-requirement-grade` 内输出协作简报和门禁，至少需要研发影响面评估、测试/设计验收和上线观察；复杂规则再转 `pm-prd-write`；若要求设计前评估页面效果，追加页面内容契约、代表性数据、`prototypeReadiness` 和静态 HTML / SVG 交付约束。
- L3：在 `pm-requirement-grade` 内输出 PRD/spec 评审门禁和交接摘要；完整 PRD 必须进入 `pm-prd-write`；需要 UX 原型时，必须沿 `prototypeTarget → pageSchema/contentContract → prototypeReadiness → pm-prd-html` 传递，不能由设计阶段补齐用户可见事实。
- H：在 `pm-requirement-grade` 内输出 hotfix 治理包，由研发/值班负责人止血，禁止产品自助修复后上线。

## 原项目安全审查

若用户要求“兴趣岛/XQD 检查代码”“兴趣岛规范”“审核代码”“安全审查”，或上线前需要 Vibe Coding 安全审查，使用现有 `xqd-vc-dev` skill；该安全审查通过不代表可以绕过 L2/L3 分级。
