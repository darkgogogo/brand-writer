# 封面图固定模板（V4，2026-05-08 起）

本工作流所有文章封面使用统一的 V7-style prompt 模板，保证品牌一致性。

**V4 变更（2026-05-08）**：模板从 V3 的 Subject-only 简单结构升级为 V7 的 7 段完整 prompt 结构（来源：实测用 ChatGPT 客户端反向工程出的 prompt，输出质量高于 V3）。原因：博客封面需要"主物件 + 辅助 4 元素 + 顶部徽章 + 标题文字排版"的固定结构，简单 Subject 模板不足以驱动稳定输出。

> ⚠️ 即使用同一 prompt，**OpenAI API gpt-image-1 输出明显次于 ChatGPT 客户端**（客户端有隐式 prompt enhancer / 智能 size / 可能 N 选 1 重试）。因此本模板**首选 Path A（用户拿 prompt 去 ChatGPT 客户端等外部工具生成）**，Path B（API 自动）作为简单场景的备选。

## 固定 Prompt 模板

每篇封面使用以下 7 段结构。变量部分用 `[占位符]` 标记，**结构和写死部分一字不动**。模板默认调色板和主物件按本工作流的参考品牌设定，若你自己的产品有不同品牌色，按下文「品牌可改部分」调整。

```
Create a 16:9 flat vector illustration for a [PRODUCT_DOMAIN] [ARTICLE_KIND].

Style:
Modern tech-editorial blog cover illustration. Clean flat vector design. Solid filled background color #EEEEFE covering the entire canvas. Do NOT use a transparent background. The background must be a solid flat color fill, not white. Limited color palette: deep navy blue #1a1a3e, white, soft lavender-purple #b8b5ff, and small coral-orange accents. All objects must have visible black outlines and black strokes on every main shape. Purely flat illustration, no gradients, no 3D effects, no shadows, no realistic textures.

Main concept:
[MAIN_CONCEPT：一句英文描述本篇核心主题，30-50 词]

Composition:
Centered compact 16:9 composition. A large laptop screen in the center is the main object. On the laptop screen, show a bold headline in deep navy uppercase text:

[HEADLINE_LINE_1]
[HEADLINE_LINE_2]

The text should be clean, readable, and spelled exactly as "[HEADLINE_FULL]".

Inside the laptop screen, add a small [PRODUCT_ICON] icon and a short supporting line of text: "[SUBTITLE_EN]". Keep the small text secondary and minimal.

Surrounding elements:
To the left of the laptop, place a [LEFT_ELEMENT]. To the right of the laptop, place a [RIGHT_ELEMENT_BACK]. In front of the chart, place a [RIGHT_ELEMENT_FRONT].

Top center:
Add a circular checkmark badge above the laptop screen, indicating successful restoration.

Visual details:
Use simple geometric shapes, thick black outlines, rounded corners, clean icon-like forms. Add a few tiny decorative dots and plus signs scattered very sparsely around the composition. Keep the image uncluttered with a maximum of four main visual elements: laptop, [LEFT_NAME], [RIGHT_BACK_NAME], [RIGHT_FRONT_NAME].

Restrictions:
No people, no human characters, no hands, no faces. No photorealism. No 3D. No shadows. No gradients. No transparent background. No extra text besides "[HEADLINE_FULL]" and optionally "[SUBTITLE_EN]." Ensure the image looks like a polished technology blog article cover.
```

## 变量填写规范

| 变量 | 说明 | 示例（主题：「产品恢复正常运营」） |
|---|---|---|
| `[PRODUCT_DOMAIN]` | 产品所在领域，1-3 词 | `VPN service` / `AI tool` / `SaaS app` |
| `[ARTICLE_KIND]` | 文章类型，1-3 词 | `status announcement` / `feature update` / `troubleshoot guide` |
| `[MAIN_CONCEPT]` | 一句英文描述本篇主题，30-50 词 | "A VPN service had an outage or technical issue for a period of time and has now returned to normal operation." |
| `[HEADLINE_LINE_1]` / `[HEADLINE_LINE_2]` | 笔记本屏幕主标题，分两行的英文短词，全大写 | `SERVICE` / `RESTORED` |
| `[HEADLINE_FULL]` | 同上但单行（用于 Restrictions 段引用） | `SERVICE RESTORED` |
| `[SUBTITLE_EN]` | 屏幕下方副标题，简短英文一句（建议 ≤10 词） | `The VPN service is back online.` |
| `[PRODUCT_ICON]` | 产品代表性 icon（一个名词词组） | `VPN shield` / `AI robot` / `cloud sync` |
| `[LEFT_ELEMENT]` | 笔记本左侧辅助元素描述（建议含 symbolizing 子句） | `large gear icon with circular refresh arrows inside, symbolizing system recovery and restart` |
| `[RIGHT_ELEMENT_BACK]` | 笔记本右侧后景元素 | `rising bar chart with a coral-orange upward arrow, symbolizing service recovery and normal operation` |
| `[RIGHT_ELEMENT_FRONT]` | 右侧前景遮挡元素 | `protection shield with a deep navy checkmark, symbolizing secure protection restored` |
| `[LEFT_NAME]` / `[RIGHT_BACK_NAME]` / `[RIGHT_FRONT_NAME]` | 上述元素的简称（用于 Visual details 段汇总） | `gear/recovery icon` / `rising chart` / `security shield` |

## 写死规则（结构性，任何品牌都不要改）

以下是 V7 prompt 模板的**结构骨架**，任何品牌使用本模板都不要改：

- **7 段分块结构**：Style / Main concept / Composition / Surrounding elements / Top center / Visual details / Restrictions
- **比例宣告**：开篇 `Create a 16:9 flat vector illustration for a ...`
- **主元素数量上限**：4 个主视觉（laptop + 左 + 右后 + 右前），不增不减
- **笔记本主体**：中心主物件固定为 laptop（屏幕承载文字排版）
- **顶部 ✓ 徽章**：固定的"成功/正常"信号锚点
- **Restrictions 段**：禁止人物、3D、阴影、渐变等约束保留

## 品牌可改部分（每个产品可自定义）

如果你的品牌色 / 主视觉与默认模板不一致，可以改这些字段，**改完后写进自己的 product profile 作为该产品的固定 cover 参数**：

| 可改字段 | 默认值（参考品牌） | 改的时候注意 |
|---|---|---|
| **背景色** | `#EEEEFE`（淡紫白） | 选一个浅色调，与品牌主色互补 |
| **调色板** | `#1a1a3e`（深蓝）/ white / `#b8b5ff`（淡紫）/ coral-orange accents | 建议保持 4 色限定（深主色 + 白 + 浅辅色 + 强调色） |
| **`[PRODUCT_ICON]`** | `VPN shield` | 换成你产品的标志性 icon |
| **`[PRODUCT_DOMAIN]` 默认值** | `VPN service` | 改成你产品领域 |
| **`[ARTICLE_KIND]`** | `status announcement` | 按本篇文章类型填 |

> 建议你写一份「我们品牌的 cover-template overrides」放进产品 profile，把上面 5 个可改字段固化，每篇文章只填变化部分（MAIN_CONCEPT / HEADLINE / SUBTITLE / LEFT/RIGHT_ELEMENT）。

## 适用范围

本 V4 模板针对**服务公告 / 状态变更 / 故障排查类**文章设计。其他文章原型（科普 / 调查实验 / 现象解读）使用本模板时若发现核心物件（laptop）与主题违和，可在后续版本扩展平行模板（如 `cover-template-science.md`）。当前 v4 阶段**不分类、不分歧**，统一用本模板验证模板稳定性后再考虑扩展。

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
- **V4**（2026-05-08）：迁移到 V7-style 7 段完整 prompt 模板 + Path A/B 双路径。本版起以 V7-style 为唯一封面规范。
