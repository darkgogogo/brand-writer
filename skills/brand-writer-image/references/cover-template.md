# 封面图固定模板

本工作流所有文章封面使用同一套视觉语言，保证品牌一致性。

## 固定 Prompt 模板（V2 重写：约束前置，Subject 后置）

```
Flat vector illustration. Solid fill colors only, NO gradients, NO 3D, NO shadows, NO texture. Solid flat background color #EEEEFE covering the entire canvas, not transparent not white. Limited palette only: deep navy #1a1a3e, pure white, soft lavender #b8b5ff, small coral-orange accents. One stylized human character with DOT EYES (two small dots) and NO MOUTH, minimalist face, clean black outlines. Centered composition, compact layout, maximum 3 main objects total, very sparse tiny decorative dots. Modern tech-editorial style. Subject: [根据文章核心关键词生成的场景描述，1-2 句英文，主体图标/物件 + 人物姿态/情绪]
```

**结构说明**（为什么这样排）：Recraft V3 对 prompt 前半段权重更高，因此所有硬约束（flat/无渐变/背景色/配色/人物五官/物件数）全部前置；Subject 放在最后，避免模型读到 Subject 后忽视前面的约束。

## 可变字段

**只有 Subject 部分**每篇不同。其他所有文字完全一致（包括大小写、标点、空格）。

**Subject 生成规则**：
- 1-2 句英文
- 含主体图标/物件（VPN 服务器、AI 机器人、盾牌等）
- 含人物姿态/情绪（confused / relieved / focused / surprised / worried 等）
- 与文章核心关键词强相关
- **不要**在 Subject 里再写风格词（如 flat / vector / dot eyes 等），前置约束已覆盖

### Subject 示例

- 文章主题「VPN 封号」→ `A stylized VPN server shield with a small warning sign, and a worried person looking at a laptop screen showing an access-denied message.`
- 文章主题「AI 友好节点」→ `A stylized globe with glowing connection nodes, and a focused person at a desk chatting with an AI assistant on screen.`
- 文章主题「VPN 频繁断线」→ `A wall-mounted server rack with one ethernet cable being unplugged, and a person standing beside it with raised hands in a questioning pose.`

## 固定参数

- **style**: `digital_illustration`（V2 曾尝试切到 `vector_illustration` 以强制 flat，但返回 SVG 不可直接预览、且依赖本机 `rsvg-convert` 太脆，回切。flat 效果改由 prompt 前置约束保证）
- **image_size**: `landscape_16_9`（社媒封面通用比例）
- **输出**：API 原生 PNG/WebP，无需任何本地转换工具

## 文件名

封面图统一保存为 `cover.png`。

## 英文版文章的封面

英文版 cover prompt 模板完全一样（英文本身就是一套），Subject 按英文文章内容重新构思。

## 禁止修改

以下字段任何时候都不要改（视觉一致性约束）：
- 背景色 `#EEEEFE`
- 配色 `#1a1a3e` / pure white / `#b8b5ff` / coral-orange
- 人物五官 `DOT EYES and NO MOUTH`
- 禁止元素 `NO gradients, NO 3D, NO shadows, NO texture`
- style 参数 `digital_illustration`

## 如果生成图仍不符合模板

优先尝试：
1. 重新生成（同一 prompt 多试几次，`digital_illustration` 偶尔会出意外风格，前置约束已经是最强防线）
2. 检查 Subject 是否包含了破坏 flat 约束的词（如 `realistic`、`photo`、`shadow`、`3d`）—— 去掉
3. 若多次重生成仍错，在 Subject 前加一次强化：`Strictly flat icon style.` 然后接 Subject
