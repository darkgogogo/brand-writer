# 产品档案 schema

位置：`~/.claude/skills/brand-writer/profiles/<产品名>.md`

文件名约定：产品英文短名，小写（无空格，可用连字符）。如 focusflow.md、my-product.md。

## 标准结构

```markdown
---
name: <产品英文短名，小写>
display_name_zh: <中文正式名>
display_name_en: <英文正式名>
---

## 产品定位
一句话描述产品做什么、服务谁。

## 目标用户
具体画像：职业 / 年龄段 / 使用场景 / 技术水平。

## 核心场景
- 场景 1：用户具体在做什么
- 场景 2
- 场景 3

## 核心痛点库
写作时可直接引用的痛点沉淀。每条含：
- 现象（用户感知到什么）
- 根因（为什么发生）
- 后果（如果不解决会怎样）

## 技术关键词
可直接用的专业表述，避免 AI 用词泛化。

## 品牌规则
- 中文名 / 英文名 / 混排名约定
- 正文人称使用规则
- 禁用自称（博主专属，绝不迁移）
- 其他品牌声音边界

## 联系方式
- 客服邮箱
- 其他官方渠道

## 写作偏好
- 标题风格
- 开篇规则
- 类比原则（技术机制转化为生活化类比的要求）
- 节奏偏好（短句优先 / 操作指南招数数量上限）

## 禁用话题（可选）
- 不能提的竞品名
- 敏感话题

## 封面默认值
<!-- 配合 brand-writer-image V4.1 模板的「品牌级变量」。写稿时 brand-writer-article 直接读这里 inherit，每篇只填"每篇必填"那 8 个字段。改这里 → 所有本产品封面统一切调。无此 section 则 fallback 到 cover-template.md 末尾的「参考品牌默认」。 -->

- BG_COLOR: `<背景纯色 hex 或描述>`
- PRIMARY_COLOR: `<主深色，标题文字用>`
- SECONDARY_COLOR: `<辅深色，通常 white>`
- TERTIARY_COLOR: `<辅浅色>`
- ACCENT_COLOR: `<强调色>`
- MAIN_OBJECT: `<中心主物件，如 large open notebook / large laptop screen>`
- MAIN_OBJECT_SURFACE: `<标题文字落在哪，如 the left page / the laptop screen>`
- MAIN_OBJECT_NAME: `<上述物件的简称，用于 Visual details 段汇总>`
- PRODUCT_ICON: `<产品代表 icon，如 flower / VPN shield>`
- TOP_BADGE_SHAPE: `<顶部徽章形状，如 crescent moon badge / circular checkmark badge>`
- TOP_BADGE_SEMANTIC: `<徽章语义，如 deep focus mode / successful restoration>`

## 豁免词
<!-- 可选 section。若无豁免词可整段省略；登记后格式：- <词>：<理由>（经 review 后生效，brand-writer-check L1 Layer B 会直接从词表剔除）-->
- <词1>：<豁免理由>
- <词2>：<理由>
```

**豁免词说明**：
- 用于登记本产品专属的"官方术语"——即使词在 `brand-writer-check/references/banned-words.md` 🔴/🟡 列表里，登记后也**直接跳过匹配**（不报、不提示）
- 格式详见 `brand-writer-check/references/banned-words.md` 的「3. 优先级」section
- 例：focusflow 的官方文案「深度专注模式」长期使用"深度"一词，可登记豁免

**封面默认值说明**：
- 配合 `brand-writer-image/references/cover-template.md` 的 V4.1 模板使用
- 把封面 prompt 的变量分两层：**Layer 1 品牌级**（这 11 个字段，profile 里写一次，所有文章 inherit）vs **Layer 2 每篇必填**（`[MAIN_CONCEPT]` / `[HEADLINE_*]` / `[SUBTITLE_EN]` / 3 个 surrounding elements 等，每篇文章写稿时填）
- 改了这 section 之后所有新稿的封面统一切到新调；老稿的「封面图 Prompt」section 已经填好不会回溯
- 若 profile 完全不写本 section，brand-writer-article 在生成 cover prompt 时回退到 `cover-template.md` 末尾的「参考品牌默认」（letsvpn 原值）

## 字段级说明

**name**：小写英文短名，是 skill 引用档案的 key。
**display_name_zh / display_name_en**：用户面对的正式产品名，会出现在稿件中。
**人称规则**：例如 focusflow 规定只用「我们」和「你」，禁用「小编」「XX君」等。
**禁用自称**：模仿博主时，博主的专属自称（如「差评君」「差友」）必须禁用以避免身份错乱。
**封面默认值**：11 个字段一组（5 色 + 3 主物件字段 + 产品 icon + 2 徽章字段），写一次决定本产品所有封面的视觉语言；具体字段语义见 `cover-template.md` 的「变量填写规范」表。
