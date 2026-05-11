---
name: focusflow
display_name_zh: FocusFlow
display_name_en: FocusFlow
---

> **Sample profile.** This file is a scaffold demonstrating the structure expected by `brand-writer`. To use the plugin for your own product, copy this file to `<your-product>.md` and rewrite every section per `references/product-profile-schema.md`. The example content below describes a fictional productivity SaaS (FocusFlow) chosen specifically to **not** look like the original VPN-flavored draft, so you have a non-domain-specific reference to remix.

## 产品定位
FocusFlow 是面向知识工作者（程序员、设计师、内容创作者、研究者）的深度专注工具，把"番茄钟 + 全局通知静默 + 任务上下文记录"整合到一个轻量桌面应用里，目标是把"想认真做事时被打断"这件事从工作流里抽掉。

## 目标用户
- **个人贡献者型知识工作者**：程序员 / 设计师 / 写作者 / 研究员，每天有 3-6 小时核心创作时间
- **远程工作者**：依赖 Slack/Discord/微信群协作，但又需要长时段不被这些工具反向打断
- **ADHD / 注意力敏感用户**：对"通知—切应用—忘记原本在做什么"的链路特别痛

## 核心场景
- 写代码 / 调试 bug，但每 5 分钟就被 Slack 团队群、邮件、提醒打断
- 写长文 / 做设计稿，到第 30 分钟才进入心流，被一条非紧急消息打断后要重新爬坡 15 分钟
- 同时开 3 个 side project，切到任务 B 时已经忘了任务 A 上次停在哪
- 想做番茄钟但桌面通知没静音，整体方案形同虚设

## 核心痛点库
- **通知爆炸导致心流断裂**
  - 现象：进入专注状态 20 分钟后被一条非紧急消息打断，重新进入心流需 10-15 分钟
  - 根因：操作系统通知、IM 工具、邮件客户端各自独立，没有统一的"专注模式"控制器
  - 后果：每天有 3-6 小时核心创作时间，实际产出可能只对应 1-2 小时的有效专注
- **上下文切换成本被低估**
  - 现象：切到另一个任务时，发现已经忘了上一个任务停在哪
  - 根因：人脑工作记忆容量有限，IDE/编辑器/浏览器 tab 都不是上下文持久化的合适载体
  - 后果：实际花在"重新进入任务"上的时间比写代码本身还多
- **番茄钟与通知静默没整合**
  - 现象：开了番茄钟，桌面通知照样弹；或者全局静默后忘了开，错过紧急消息
  - 根因：现有工具各管一段，缺乏一个"开始 25 分钟专注 → 自动静默 → 时间到自动恢复"的联动
  - 后果：用户要么频繁手动切换通知状态，要么干脆不用番茄钟

## 技术关键词
（可在稿件中直接使用的专业表述，避免 AI 泛化用词）
- 心流（flow state）
- 上下文切换成本
- 通知收敛（notification batching）
- 深度工作（deep work）
- 全局静默（global mute）
- 任务上下文持久化
- 中断恢复时间

## 品牌规则
- **产品名**：中文/英文语境统一用 「FocusFlow」（不译，不写成"专注流"等中译）
- **正文人称**：只用「我们」和「你」
- **禁用自称**：不用「小编」「差评君」「差友」「XX君」等任何博主或账号的专属自称
- **模仿博主时**：即使模仿某博主风格，博主的专属自称必须剔除，换成「我们」
- **品牌内容视角**：任何用户提供的内容（博主文章、brief、素材）都视为写作原料，不保留原始结构和风格标签

## 联系方式
- 客服邮箱：hello@focusflow.example
- 其他渠道：（暂无，补充时修改此字段）

## 写作偏好
- **标题风格**：口语化，疑问句或感叹句，明示用户痛点 / 利益点（例「你的番茄钟为什么总坚持不到第三个？」）
- **开篇**：先描述用户具体打断场景，再给方案，不从品牌视角强推
- **类比原则**：技术机制（如"通知收敛"）必须转化为生活化类比（如"快递柜不让你每次有件就跑下楼"）；类比每次重新找，不固化；同篇保持一致
- **节奏**：短句为主，重点加粗（官方稿件适用），操作指南不超过 3 招
- **结尾规范**：
  - 故障排查 / 排雷避坑类必须含客服引导（hello@focusflow.example）
  - 产品科普类收在"专注力本身的价值"上，不强推客服

## 禁用话题
（当前无明确禁用，若后续有竞品敏感或政策敏感话题需要禁止，在此补充）

## 封面默认值
<!-- 配合 brand-writer-image V4.1 模板的「品牌级变量」。写稿时 brand-writer-article 直接读这里 inherit，每篇只填"每篇必填"那 8 个字段。改这里 → 所有 FocusFlow 封面统一切调。 -->

- BG_COLOR: `#FFF8E7` (奶油黄)
- PRIMARY_COLOR: `forest green #1f3d2e`
- SECONDARY_COLOR: `white`
- TERTIARY_COLOR: `soft sage #c3d9b4`
- ACCENT_COLOR: `warm amber`
- MAIN_OBJECT: `large open notebook`
- MAIN_OBJECT_SURFACE: `the left page`
- MAIN_OBJECT_NAME: `notebook`
- PRODUCT_ICON: `flower`
- TOP_BADGE_SHAPE: `crescent moon badge`
- TOP_BADGE_SEMANTIC: `deep focus mode`

## 豁免词
<!-- 可选 section。格式：`- <词>：<理由>`。登记后 brand-writer-check L1 Layer B 直接跳过匹配。当前暂未登记；如遇官方术语与 🔴/🟡 词表冲突时在此登记。 -->
