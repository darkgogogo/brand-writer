# 封面图固定模板（V4.1，2026-05-11 起）

本工作流所有文章封面使用统一的 V7-style prompt 模板，保证品牌一致性。

**V4.1 变更（2026-05-11）**：把原 V4 写死在结构里的 `laptop` 主物件、`circular checkmark badge`、`indicating successful restoration` 拆出来变成 **profile 可覆盖变量**——任何品牌都能复用结构骨架，把主物件 / 顶部徽章 / 调色板换成自己的视觉语言。原 V4 默认值（laptop + ✓ + 深蓝白调）作为"参考品牌默认"保留在文末。

**V4 变更（2026-05-08）**：模板从 V3 的 Subject-only 简单结构升级为 V7 的 7 段完整 prompt 结构（来源：实测用 ChatGPT 客户端反向工程出的 prompt，输出质量高于 V3）。原因：博客封面需要"主物件 + 辅助 4 元素 + 顶部徽章 + 标题文字排版"的固定结构，简单 Subject 模板不足以驱动稳定输出。

> ⚠️ 即使用同一 prompt，**OpenAI API gpt-image-1 输出明显次于 ChatGPT 客户端**（客户端有隐式 prompt enhancer / 智能 size / 可能 N 选 1 重试）。因此本模板**首选 Path A（用户拿 prompt 去 ChatGPT 客户端等外部工具生成）**，Path B（API 自动）作为简单场景的备选。

## 固定 Prompt 模板

每篇封面使用以下 7 段结构。变量部分用 `[占位符]` 标记，**结构和 写死部分一字不动**。

```
Create a 16:9 flat vector illustration for a [PRODUCT_DOMAIN] [ARTICLE_KIND].

Style:
Modern tech-editorial blog cover illustration. Clean flat vector design. Solid filled background color [BG_COLOR] covering the entire canvas. Do NOT use a transparent background. The background must be a solid flat color fill, not white. Limited color palette: [PRIMARY_COLOR], [SECONDARY_COLOR], [TERTIARY_COLOR], and small [ACCENT_COLOR] accents. All objects must have visible black outlines and black strokes on every main shape. Purely flat illustration, no gradients, no 3D effects, no shadows, no realistic textures.

Main concept:
[MAIN_CONCEPT：一句英文描述本篇核心主题，30-50 词]

Composition:
Centered compact 16:9 composition. A [MAIN_OBJECT] in the center is the main object. On the [MAIN_OBJECT_SURFACE], show a bold headline in [PRIMARY_COLOR] uppercase text:

[HEADLINE_LINE_1]
[HEADLINE_LINE_2]

The text should be clean, readable, and spelled exactly as "[HEADLINE_FULL]".

On/near the [MAIN_OBJECT], add a small [PRODUCT_ICON] icon and a short supporting line of text: "[SUBTITLE_EN]". Keep the small text secondary and minimal.

Surrounding elements:
To the left of the [MAIN_OBJECT], place a [LEFT_ELEMENT]. To the right, place a [RIGHT_ELEMENT_BACK]. In front, place a [RIGHT_ELEMENT_FRONT].

Top center:
Add a [TOP_BADGE_SHAPE] above the [MAIN_OBJECT], indicating [TOP_BADGE_SEMANTIC].

Visual details:
Use simple geometric shapes, thick black outlines, rounded corners, clean icon-like forms. Add a few tiny decorative dots and plus signs scattered very sparsely around the composition. Keep the image uncluttered with a maximum of four main visual elements: [MAIN_OBJECT_NAME], [LEFT_NAME], [RIGHT_BACK_NAME], [RIGHT_FRONT_NAME].

Restrictions:
No people, no human characters, no hands, no faces. No photorealism. No 3D. No shadows. No gradients. No transparent background. No extra text besides "[HEADLINE_FULL]" and optionally "[SUBTITLE_EN]." Ensure the image looks like a polished technology blog article cover.
```

## 变量填写规范

### 每篇文章必填（写稿时确定）

| 变量 | 说明 | 示例 |
|---|---|---|
| `[PRODUCT_DOMAIN]` | 产品所在领域，1-3 词 | `productivity tool` / `VPN service` / `design app` |
| `[ARTICLE_KIND]` | 文章类型，1-3 词 | `feature update` / `troubleshoot guide` / `status announcement` |
| `[MAIN_CONCEPT]` | 一句英文描述本篇主题，30-50 词 | "A productivity app reducing context-switching by silencing distracting notifications during deep work sessions." |
| `[HEADLINE_LINE_1]` / `[HEADLINE_LINE_2]` | 主标题，分两行的英文短词，全大写 | `DEEP` / `FOCUS` |
| `[HEADLINE_FULL]` | 同上但单行（用于 Restrictions 段引用） | `DEEP FOCUS` |
| `[SUBTITLE_EN]` | 副标题，简短英文一句（≤10 词） | `Silence the noise. Ship the work.` |
| `[LEFT_ELEMENT]` / `[RIGHT_ELEMENT_BACK]` / `[RIGHT_ELEMENT_FRONT]` | 3 个辅助元素描述（建议含 symbolizing 子句） | `headphone icon symbolizing focus`; `bell with slash through it symbolizing muted notifications`; `clock with progress ring symbolizing pomodoro` |
| `[LEFT_NAME]` / `[RIGHT_BACK_NAME]` / `[RIGHT_FRONT_NAME]` | 上述元素的简称（用于 Visual details 段汇总） | `headphones` / `muted bell` / `pomodoro clock` |

### 品牌级（每个产品的 profile 里固化一次，写稿时直接 inherit）

| 变量 | 说明 | letsvpn 默认值 | FocusFlow 示例 |
|---|---|---|---|
| `[BG_COLOR]` | 背景纯色 | `#EEEEFE` (淡紫白) | `#FFF8E7` (奶油黄) |
| `[PRIMARY_COLOR]` | 主深色（标题文字用） | `deep navy blue #1a1a3e` | `forest green #1f3d2e` |
| `[SECONDARY_COLOR]` | 辅深色 | `white` | `white` |
| `[TERTIARY_COLOR]` | 辅浅色 | `soft lavender-purple #b8b5ff` | `soft sage #c3d9b4` |
| `[ACCENT_COLOR]` | 强调色 | `coral-orange` | `warm amber` |
| `[MAIN_OBJECT]` | 中心主物件 | `large laptop screen` | `large open notebook` |
| `[MAIN_OBJECT_SURFACE]` | 标题文字落在哪 | `the laptop screen` | `the left page` |
| `[MAIN_OBJECT_NAME]` | Visual details 段汇总用的简称 | `laptop` | `notebook` |
| `[PRODUCT_ICON]` | 产品代表性 icon | `VPN shield` | `flower` |
| `[TOP_BADGE_SHAPE]` | 顶部徽章形状 | `circular checkmark badge` | `crescent moon badge` |
| `[TOP_BADGE_SEMANTIC]` | 顶部徽章语义 | `successful restoration` | `deep focus mode` |

**建议做法**：把品牌级 12 个字段固化进产品 profile（如 `## 封面默认值` section），写稿时只填上方"每篇必填"那 8 个字段。

## 写死规则（结构性，任何品牌都不要改）

以下是 V7 prompt 模板的**结构骨架**，任何品牌使用本模板都不要改：

- **7 段分块结构**：Style / Main concept / Composition / Surrounding elements / Top center / Visual details / Restrictions
- **比例宣告**：开篇 `Create a 16:9 flat vector illustration for a ...`
- **主元素数量上限**：4 个主视觉（主物件 + 左 + 右后 + 右前），不增不减
- **顶部徽章存在性**：必须有一个 top center 徽章作为视觉锚点（形状/语义可换，存在性不可去）
- **Restrictions 段**：禁止人物、3D、阴影、渐变等约束保留
- **flat vector + 黑色描边 + 4-color limited palette + 装饰点稀疏**：这些 style 约束保留，颜色具体值可换

## 参考品牌默认（letsvpn 当前值，新品牌可整套替换）

V4 原版的默认值集中在这里展示，方便新品牌对照换：

```
[BG_COLOR]          = #EEEEFE
[PRIMARY_COLOR]     = deep navy blue #1a1a3e
[SECONDARY_COLOR]   = white
[TERTIARY_COLOR]    = soft lavender-purple #b8b5ff
[ACCENT_COLOR]      = coral-orange
[MAIN_OBJECT]       = large laptop screen
[MAIN_OBJECT_SURFACE] = the laptop screen
[MAIN_OBJECT_NAME]  = laptop
[PRODUCT_ICON]      = VPN shield
[TOP_BADGE_SHAPE]   = circular checkmark badge
[TOP_BADGE_SEMANTIC] = successful restoration
```

新产品想完整换一套时，复制这块到 profile 的 `## 封面默认值` section，逐字段改即可。

## 适用范围

本 V4.1 模板覆盖**服务公告 / 状态变更 / 故障排查 / 功能更新 / 产品科普**类文章。其他原型（如行业现象解读、长篇调查实验）如果"中心主物件"难以选定，可在后续版本扩展平行模板（如 `cover-template-narrative.md` 用更抽象的中心元素）。当前阶段统一用本模板验证稳定性后再考虑扩展。

## Path 选择建议

| Path | 推荐场景 | 操作 |
|---|---|---|
| **A**（外部工具，**首选**） | 所有品牌封面（实测质量明显高） | skill 输出本模板填空后的完整 prompt → 用户拿到 ChatGPT 客户端 / Midjourney 生成 → 回贴绝对路径 |
| **B**（API 自动，备选） | 用户暂时无 ChatGPT 客户端 / 批量复跑 / 简单图标级 | skill 直调 `gpt-image-1`，size 1536×1024，quality high，再 sips crop 16:9 |

## API 调用参数（仅 Path B 用）

| 参数 | 值 | 说明 |
|---|---|---|
| `--size` | `1536x1024` | OpenAI 不支持 16:9，先生成 3:2 再 sips crop |
| `--quality` | `high` | 品牌封面必选高质量（~$0.17/张） |
| `--output-format` | `png` | 默认 |

## 后处理：sips crop 到 16:9（Path A/B 共用）

```bash
# 1536×1024 (3:2) → 1536×864 (16:9)
sips -c 864 1536 cover.png --out cover.png
```

`sips -c HEIGHT WIDTH` 是 macOS 自带工具，零依赖。`-c` 是中心裁剪。

> Path A：先用 `sips -g pixelWidth pixelHeight` 检测用户回流图的比例，若已是 16:9（容差 ±2px，例：1456×816 / 1672×941 / 1792×1008 都视为 16:9），跳过 crop；非 16:9 才执行裁剪。

## 文件名

封面图统一保存为 `cover.png`。最终尺寸保留为生成图原比例后裁出的 16:9（典型为 1536×864 或 1672×941，取决于工具）。

## 英文版文章的封面

英文版 cover prompt 模板完全一样（本模板本身就是英文）。中英文版可共用同一个 cover.png（封面是文章级别的，不分语言）。

## 已知局限 / 容忍

- API gpt-image-1 偶尔会在主体物件上加少量计划外文字。可在 prompt 末尾加一句 `Absolutely no extra text other than the specified headline and subtitle.`
- API 偶尔会加少量装饰（小叶子、小星星、小点点），通常无害；要严格控制可在 Visual details 段末加 `NO leaves, NO plants, NO clouds, only the four listed elements and the tiny decorative dots/plus signs.`
- ChatGPT 客户端（Path A）一般不需要这些 fallback 调整。

## 历史

- **V1/V2**（2026-05-05）：fal.ai 时代 Subject-only 模板 + DOT EYES 人物风格。已 deprecated。
- **V3**（2026-05-06）：fal → OpenAI gpt-image-1 切换；Subject-only 模板保留。已 deprecated。
- **V4**（2026-05-08）：迁移到 V7-style 7 段完整 prompt 模板 + Path A/B 双路径。`laptop` / 顶部 ✓ 徽章 / 调色板写死在结构里。
- **V4.1**（2026-05-11）：把 `[MAIN_OBJECT]` / `[TOP_BADGE_*]` / 5 个颜色字段提为 profile 级变量，结构骨架真正中性化；letsvpn 原值作为"参考品牌默认"展示。
