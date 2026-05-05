---
name: brand-writer-image
description: |
  为品牌文章生成封面和正文配图，调用 fal.ai Recraft V3 text-to-image API。用户说"生成配图"、"出图"、"画一下"、"配图生成"时触发。封面用固定模板（深蓝白+淡紫+珊瑚橙），正文配图 6 种风格可选。所有图均为 PNG 原生输出，无外部依赖。图片保存到文章的 images/ 子目录。需要环境变量 FAL_API_KEY。不要用于其他项目（只服务本工作流的文章）。
---

# brand-writer-image 配图生成 skill

> 本 skill 依赖 `~/.claude/skills/brand-writer/references/constants.md` 的共享常量（路径规则）。

调 fal.ai Recraft V3 API 生成封面和正文配图。

## 输入

- 文章路径（`$BRAND_WRITER_HOME/articles/<名>/<名>.md`）
- **前提**：同目录 `self-check-report.md` 末尾必须有 `**人工审阅**：✅ 通过` 一行（V2 gate，D13，与 brand-writer-social 一致）

读出文章中的「封面图 Prompt」和各 "📷 **配图建议**" 段落。

## 流程

### Step 0: 人工审阅 gate 校验（V2，D13）

Read `articles/<名>/self-check-report.md`，检查末尾是否含 `**人工审阅**：✅ 通过`：
- **无** → 拒绝执行，回复用户：
  > ❌ 未检测到人工审阅通过标记。
  > 请先打开 `articles/<名>/self-check-report.md` 审阅，确认无误后告诉我"审阅通过"，我再继续生成配图。
- **有** → 进 Step 1

### 1. 选正文配图风格

先更新 `_session.json.stage` → `image_gen`（运行中标记，本 skill 全部成功收尾后切回 `idle`；若用户明确说结束则 `done`）。

封面图使用固定模板，**不参与风格选择**。向用户问正文配图的风格（6 种，全部 PNG 原生输出）：

```
请选择正文配图风格（全文统一）：

1. 数字插画      — 现代清晰，科技/科普类首选
2. 2D 海报       — 版式感强，品牌视觉
3. 手绘插画      — 温暖亲切，场景/故事类
4. 颗粒质感      — 层次丰富，深度叙事类
5. 手绘线稿      — 轻盈简洁，概念草图感
6. 自然光写实    — 真实感强，场景氛围类

输入数字选择（默认 1）：
```

风格对应的 Recraft V3 style 参数（详见 references/style-options.md）：
- 1 → `digital_illustration`
- 2 → `digital_illustration/2d_art_poster`
- 3 → `digital_illustration/hand_drawn`
- 4 → `digital_illustration/grain`
- 5 → `digital_illustration/hand_drawn_outline`
- 6 → `realistic_image/natural_light`

> V2 变更：原 6/7（line_art / line_circuit，`vector_illustration/*`）返回 SVG 无法直接预览，已移除。如需矢量线条风格，另起独立流程处理（暂未支持）。

### 2. 转写英文 Prompt

**封面图**：直接从文章的「封面图 Prompt」section 原文复制到 Python 调用的 `prompt` 参数，**不做任何修改**。封面 API 调用固定使用 `digital_illustration` style（V2 曾切到 vector 但返回 SVG 不可预览，已回切；flat 效果完全由 prompt 前置约束保证，详见 `references/cover-template.md`）。

**正文配图**：
- 直接用名词短语描述画面主体、场景、构图，30-50 词
- **不写风格词**（由 style 参数统一控制）
- 结尾统一加：`clean background, no text, no real human faces`
- 色调用具体颜色词：`muted blue and grey palette`

### 3. 调 API 生成并下载

**JSON / Python 规范（严格执行）**：
- 所有字符串值使用 ASCII 直引号（`"`），禁用中文弯引号
- `desc` 字段必须是扁平字符串，禁止嵌套对象
- 执行前验证 Python 语法

**统一调用 scripts/generate_image.py**：
```bash
# 封面图（digital_illustration + 16:9，PNG 原生）
python3 ~/.claude/skills/brand-writer-image/scripts/generate_image.py \
  --prompt "[英文 prompt]" \
  --style "digital_illustration" \
  --image-size "landscape_16_9" \
  --output "$BRAND_WRITER_HOME/articles/<文章名>/images/cover.png"

# 正文配图（风格按用户选择，比例 landscape_4_3，PNG 原生）
python3 ~/.claude/skills/brand-writer-image/scripts/generate_image.py \
  --prompt "[英文 prompt]" \
  --style "[用户选的 style]" \
  --image-size "landscape_4_3" \
  --output "$BRAND_WRITER_HOME/articles/<文章名>/images/img1.png"
```

### 4. 文件命名与输出格式

- 封面：`cover.png`（16:9）
- 正文配图：`img1.png`、`img2.png`、...（4:3）

**所有可选风格 API 原生返回 PNG/WebP，无需任何本地转换工具或外部依赖**。脚本会按 API 实际格式自动纠正 `--output` 扩展名（例如 WebP 时改成 `.webp`），在 stdout 打印**真实落盘路径**（`OK: <path>`）。调用方始终传 `.png`，后续步骤**必须解析 stdout 的 OK 行**拿最终路径，不要假设扩展名。

### 5. 生成过程提示

每张图生成时告知用户进度：

```
正在生成封面图（1/4）...  ✅ 已保存至 $BRAND_WRITER_HOME/articles/<名>/images/cover.png
正在生成配图 1（2/4）...  ✅ 已保存至 $BRAND_WRITER_HOME/articles/<名>/images/img1.png
正在生成配图 2（3/4）...  ✅ 已保存至 $BRAND_WRITER_HOME/articles/<名>/images/img2.png
正在生成配图 3（4/4）...  ✅ 已保存至 $BRAND_WRITER_HOME/articles/<名>/images/img3.png

✅ 全部配图已生成并保存。
用 Finder 打开：open "$BRAND_WRITER_HOME/articles/<名>/images/"
```

## 健壮性（V2 新增，D4）

脚本对每张图做 3 次指数退避重试（间隔 2s/4s/8s）：
- HTTP 429/500/502/503/504 → 自动重试
- 网络超时 / JSON 解析错误 → 自动重试
- 4xx（非 429）→ 直接失败（prompt 本身有问题）
- 每张图成功**立即落盘**，不等其他图

失败不阻塞整批生成。最后汇总告诉用户：
> ✅ 成功 3/4，失败 1 张：cover.png (429 限流，已重试 3 次)
> 要重新生成失败的那张吗？

## 重新生成

用户可能说的命令：
- `重新生成第 N 张` → 只重新生成对应编号的图片，覆盖原文件
- `重新生成封面图` → 只重新生成 cover.png
- `换风格重新生成` → 重新询问风格，重新生成全部

## 环境变量

API Key 从环境变量 `FAL_API_KEY` 读取。如果未设置，告知用户：

> ⚠️ 未检测到 FAL_API_KEY 环境变量。
> 请在 `~/.zshrc` 中添加：`export FAL_API_KEY="你的 key"`
> 然后 `source ~/.zshrc` 后重试。

## 参考

- 封面图固定模板：references/cover-template.md
- 6 种正文配图风格详解：references/style-options.md
- Python 脚本：scripts/generate_image.py
