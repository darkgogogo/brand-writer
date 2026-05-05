# 正文配图 6 种风格详解

全文正文配图统一一种风格，启动时询问用户选择。**全部 API 原生 PNG/WebP 输出，无外部依赖**。

> V2 变更：原 6/7（`vector_illustration/line_art` / `vector_illustration/line_circuit`）返回 SVG 不可直接预览，且依赖本机 `rsvg-convert` 太脆，已移除。如需矢量线条风格，另起独立流程处理（暂未支持）。

## 1. 数字插画（默认）

**Recraft style**: `digital_illustration`

**适合**：科技/科普类文章、现代产品体验文、面向一般读者的干货
**视觉**：现代清晰、配色鲜明、层次简洁
**典型应用**：AI 工具科普、产品功能讲解

## 2. 2D 海报

**Recraft style**: `digital_illustration/2d_art_poster`

**适合**：品牌视觉、活动推广、观点表达
**视觉**：版式感强、标语感、海报质感
**典型应用**：产品发布、年度总结、重大活动

## 3. 手绘插画

**Recraft style**: `digital_illustration/hand_drawn`

**适合**：温暖/亲切/场景/故事类文章
**视觉**：手绘质感、温度感、个人叙事感
**典型应用**：用户故事、创始人写作、公司文化

## 4. 颗粒质感

**Recraft style**: `digital_illustration/grain`

**适合**：深度叙事、调查报道、长文
**视觉**：层次丰富、质感厚重、胶片感
**典型应用**：深度调查、复杂话题解读

## 5. 手绘线稿

**Recraft style**: `digital_illustration/hand_drawn_outline`

**适合**：概念草图、轻松话题、教程
**视觉**：轻盈简洁、线条优先、草图感
**典型应用**：操作教程、轻量科普

## 6. 自然光写实

**Recraft style**: `realistic_image/natural_light`

**适合**：场景氛围、真实感、纪录片式
**视觉**：真实感强、光线感、沉浸
**典型应用**：用户场景复刻、办公室场景、生活场景

## 选择逻辑参考

| 文章原型 | 推荐风格（按优先） |
|---|---|
| 故障排查 | 1 数字插画 / 5 手绘线稿 |
| 排雷避坑 | 1 数字插画 / 2 2D 海报 |
| 产品科普 | 1 数字插画 / 5 手绘线稿 |
| 调查实验 | 4 颗粒质感 / 2 2D 海报 |
| 产品体验 | 3 手绘插画 / 6 自然光写实 |
| 现象解读 | 4 颗粒质感 / 2 2D 海报 |

## 正文配图 Prompt 规范

- 30-50 词
- 只用名词短语描述画面主体、场景、构图
- **不写风格词**（由 style 参数控制）
- 结尾统一加：`clean background, no text, no real human faces`
- 色调用具体颜色词：`muted blue and grey palette`、`soft warm pastels` 等

## 图片尺寸

- 默认 `landscape_4_3`（横图，适合公众号主视觉）
- 特殊需求可用 `square_hd`（方图）、`portrait_4_3`（竖图）
- 英文版同尺寸
