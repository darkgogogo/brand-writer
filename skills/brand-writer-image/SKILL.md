---
name: brand-writer-image
description: |
  为品牌文章生成封面和正文配图。用户说"生成配图"、"配图生成"时触发。**V4（2026-05-08）**：进入流程后让用户选择路径——A=输出 prompt 由用户拿到外部工具（ChatGPT 客户端 / Midjourney / Figma 等）手动生成后回贴绝对路径、B=skill 直调 OpenAI gpt-image-1 API 自动生成。Path A 适合复杂场景叙事/带文字排版/多层次构图（外部工具质量明显优于 API），Path B 适合简单图标级或批量自动化场景。封面用固定模板 + sips crop 到 16:9；正文配图比例可选。所有图均为 PNG，仅依赖 macOS 自带 sips。图片保存到文章的 images/ 子目录。Path B 需要环境变量 OPENAI_API_KEY。不要用于其他项目（只服务本工作流的文章）。
---

# brand-writer-image 配图生成 skill

> 本 skill 依赖 `~/.claude/skills/brand-writer/references/constants.md` 的共享常量（路径规则）。

**V4 变更（2026-05-08）**：进入流程后做 fork 决策，让用户在 **Path A（外部工具）** 和 **Path B（API 自动）** 之间二选一（一篇问一次，本篇 cover + 所有正文配图统一走同一条）。Path A 是新增——把 prompt 输出给用户，用户拿到 ChatGPT 客户端 / Midjourney 等工具自己生成后回贴绝对路径，skill 负责 mv 到位 + 必要时 sips crop。原因：API gpt-image-1 vs ChatGPT 客户端虽然底模相同但行为有差异（客户端有 prompt enhancer / 智能 size / 可能 N 选 1 重试），复杂场景叙事 / 带文字排版 / 有层次的封面 ChatGPT 客户端明显更优。Path B 仍保留作为简单图标级和批量自动化场景的选项。

**V3 变更（2026-05-06）**：从 fal.ai Recraft V3 切换到 OpenAI gpt-image-1，因为 fal 在品牌封面场景下 prompt 跟随不稳定（背景色 lottery、风格 lottery）。OpenAI 在同 prompt 下一次成功，稳定可靠。

## 输入

- 文章路径（`$BRAND_WRITER_HOME/articles/<名>/<名>.md`）
- **前提**：同目录 `self-check-report.md` 末尾必须有 `**人工审阅**：✅ 通过` 一行（与 brand-writer-social 一致）

读出文章中的「封面图 Prompt」和各 "📷 **配图建议**" 段落。

## 流程

### Step 0: 人工审阅 gate 校验

Read `articles/<名>/self-check-report.md`，检查末尾是否含 `**人工审阅**：✅ 通过`：
- **无** → 拒绝执行，回复用户：
  > ❌ 未检测到人工审阅通过标记。
  > 请先打开 `articles/<名>/self-check-report.md` 审阅，确认无误后告诉我"审阅通过"，我再继续生成配图。
- **有** → 进 Step 0.5

### Step 0.5: 路径选择（V4 新增，2026-05-08）

**一篇问一次**——本篇 cover + 所有正文配图统一走同一条路径，不每张问。

对用户说：

> 本篇配图准备进入生成阶段。请选路径：
>
> **A. 外部工具**（ChatGPT 客户端 / Midjourney / Figma 等）
> 优势：复杂场景叙事 / 带文字排版 / 多层次构图明显优于 API（实测 ChatGPT 客户端 vs OpenAI API 同模型质量差距大）
> 流程：我把所有 prompt 列出 → 你拿到外部工具生成 → 把每张图的绝对路径贴回来 → 我移动到位 + 必要时 sips crop 16:9
>
> **B. API 自动**（OpenAI gpt-image-1，本 skill 直调）
> 优势：自动化、成本可控（~$0.17/cover）、可批量复跑
> 适合：简单图标级 / 几何抽象 / 已有稳定模板的场景
>
> 选 A 还是 B？

#### Path A 流程（用户选 A 时）

**A1. 标记 session**

更新 `_session.json`：
- `stage` → `image_gen`（运行中标记）
- `image_path` → `"external"`（V4 新增字段，标记本篇走外部工具，恢复时区分）

**A2. 输出所有 prompt**

逐张分块输出到对话，每张包括：
- **图编号 + 用途**（如 `[1/4] 封面`、`[2/4] 正文配图 1`）
- **完整 prompt**（封面 = 文章「封面图 Prompt」section 原文；正文 = 按 Step 2 规范从 `📷 **配图建议**` 转写产出）
- **推荐尺寸**（封面 16:9 / 1792×1024 / 1456×816 任选；正文 3:2 或自由）
- **目标命名**（`cover` / `img1` / `img2` ...，决定回流后落到哪个文件）

**A3. 输出回流提示**

```
全部 N 张 prompt 已列出。请用外部工具生成后，把每张图的绝对路径告诉我（一行一个，顺序对应上方编号）：

  /Users/.../cover-from-chatgpt.png
  /Users/.../img1.png
  ...

我会移动到 articles/<名>/images/ 并按规范重命名。封面会自动检测比例，非 16:9 时跑 sips crop 居中。
```

然后**等用户回流路径**（不超时，session 保持 `image_gen` + `image_path: external` 标记）。

**A4. 收到路径后落地**

逐张处理：
- `mv <用户给的绝对路径> articles/<名>/images/<规范命名>.png`（规范命名见 Step 5）
- 仅对 cover：先 `sips -g pixelWidth -g pixelHeight` 检测当前比例；若不是 16:9（容差 ±2px，例：1456×816 / 1792×1024 / 1536×864 都视为 16:9），跑 `sips -c <h> <w>` 中心裁剪到目标 16:9
- 报告每张最终路径

**A5. 收尾**

切 `_session.json.stage` → `idle`。`image_path: "external"` 字段保留作为本篇 image 历史记录。

#### Path B 流程（用户选 B 时）

**B1. 标记 session**

更新 `_session.json`：
- `stage` → `image_gen`
- `image_path` → `"api"`（V4 新增字段）

**B2 及之后**：走原有 Step 1-6（API 调用 + sips crop）。Step 1 的"切 stage"已在 B1 完成，重复 set 是 idempotent 安全。

#### 中断恢复（Path A/B 共用）

进入本 skill 时若 `_session.json.stage == "image_gen"`，根据 `image_path` 字段区分：

| `image_path` | 含义 | 恢复动作 |
|---|---|---|
| `"external"` | 上次走 Path A 输出了 prompt 但用户没回流路径就中断 | 问用户：(1) 重新输出 prompt 重做 / (2) 现在贴路径继续 / (3) 切 Path B 重跑 |
| `"api"` | 上次 API 跑到一半中断 | 扫 `articles/<名>/images/` 已落地的图，问用户"继续生成剩下未完成的还是重跑全部" |
| 缺失 | 老 session 字段，不区分路径 | 当成 Path B 处理（向后兼容） |

### Step 1: 准备 prompts

**OpenAI gpt-image-1 没有 style 预设参数**——所有风格描述靠 prompt 自身完成。所以不需要"6 种风格选择"那一步（V3 移除）。

封面图使用固定模板（见 `references/cover-template.md`）。
正文配图按文章里 "📷 **配图建议**" 标注内容生成。

### Step 2: 转写 prompt

**封面图**：

文章的「封面图 Prompt」section 应当**已经按 `references/cover-template.md` V4.1 模板填好**（brand-writer-article 写稿时按模板填空产出，品牌级变量从 profile 的 `## 封面默认值` section inherit，每篇必填字段写稿时确定）。本 skill 直接原文复制使用，**不做改造、不做缩短、不做风格 override**。

V4.1 模板写死了完整 7 段 prompt 结构（Style / Main concept / Composition / Surrounding elements / Top center / Visual details / Restrictions），以及**结构性约束**（flat vector 风格 / 黑色描边 / 4 主体上限 / 顶部徽章存在性 / 整段 Restrictions 禁止人物 / no 3D / no gradients）。**徽章具体形状/语义、调色板 5 色、中心主物件、产品 icon** 等品牌级元素由 profile 控制（11 个变量），不再"内置"在模板里。Step 2 只做"原文复制"动作。

> ⚠️ 若发现文章的「封面图 Prompt」section 不符合 V4.1 模板（例如只是 V3 时期的 Subject 段、或缺少 Restrictions 段、或品牌级变量未填仍是 `[BRACKET]` 占位符），停下来告诉用户："本篇封面 prompt 不符合 V4.1 模板（缺 X / 占位符未替换），是回 brand-writer-article 重生成 / 还是手动按 cover-template.md 补齐？"

**正文配图**：

按文章里 `📷 **配图建议**` 段的中文画面描述转写为英文 prompt：
- 主体描述 30-50 词
- 风格描述写在 prompt 里（如 `flat vector illustration with muted blue and grey palette, clean black outlines`）
- 结尾统一加：`clean background, no text, no real human faces`
- prompt 长度可宽松（OpenAI 容忍 4000+ chars，不像 fal ~1000 chars 硬限）

### Step 3: 调 API 生成

**JSON / Python 规范（严格执行）**：
- 所有字符串值使用 ASCII 直引号（`"`），禁用中文弯引号
- 执行前验证 Python 语法

**统一调用 scripts/generate_image_openai.py**：

```bash
# 封面图（生成 1536×1024，再 sips crop 到 16:9 = 1536×864）
SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") \
python3 ~/.claude/plugins/brand-writer/skills/brand-writer-image/scripts/generate_image_openai.py \
  --prompt "[英文 prompt]" \
  --size "1536x1024" \
  --quality "high" \
  --output "$BRAND_WRITER_HOME/articles/<文章名>/images/cover.png"

# 然后 sips crop 上下到 16:9
sips -c 864 1536 $BRAND_WRITER_HOME/articles/<文章名>/images/cover.png \
  --out $BRAND_WRITER_HOME/articles/<文章名>/images/cover.png

# 正文配图（1536×1024 landscape 3:2，正文配图不强制 16:9，3:2 也可用）
python3 ~/.claude/plugins/brand-writer/skills/brand-writer-image/scripts/generate_image_openai.py \
  --prompt "[英文 prompt]" \
  --size "1536x1024" \
  --quality "high" \
  --output "$BRAND_WRITER_HOME/articles/<文章名>/images/img1.png"
```

**Quality tier 选择**：
- `high`（默认，~$0.17/张）：品牌封面这种严要求场景必选
- `medium`（~$0.04/张）：正文配图省钱可选
- `low`（~$0.01/张）：不推荐，质量明显下降

**Size 选择**（OpenAI 不支持 16:9，只能后处理 crop）：
- `1024x1024`（1:1 square）— 用于配图无强制比例时
- `1536x1024`（landscape 3:2）— **默认**，cover + 大多数正文配图都用这个，cover 加 sips crop 到 16:9
- `1024x1536`（portrait 2:3）— 用于人像或竖排场景（罕见）

### Step 4: sips crop（macOS 内置工具，只对 cover）

OpenAI 不支持 16:9 比例，cover 需要后处理：

```bash
# 1536×1024 (3:2) → 1536×864 (16:9)，中心裁剪上下各 80px
sips -c 864 1536 input.png --out output.png
```

`sips -c HEIGHT WIDTH` 是 macOS 自带的 image 工具，零依赖。`-c` 是中心裁剪。

正文配图通常不需要 crop（3:2 直接可用），除非文章里指定了特殊比例。

### Step 5: 文件命名与输出格式

- 封面：`cover.png`（最终 1536×864 = 16:9）
- 正文配图：`img1.png`、`img2.png`、...（1536×1024 = 3:2，不 crop）

OpenAI 默认返回 PNG（脚本 `--output-format png` 默认），无 fal 时代的 WebP 自动转换问题。

### Step 6: 生成过程提示

每张图生成时告知用户进度：

```
正在生成封面图（1/4）...  ✅ 已保存至 $BRAND_WRITER_HOME/articles/<名>/images/cover.png（已 crop 16:9）
正在生成配图 1（2/4）...  ✅ 已保存至 $BRAND_WRITER_HOME/articles/<名>/images/img1.png
正在生成配图 2（3/4）...  ✅ 已保存至 $BRAND_WRITER_HOME/articles/<名>/images/img2.png
正在生成配图 3（4/4）...  ✅ 已保存至 $BRAND_WRITER_HOME/articles/<名>/images/img3.png

✅ 全部配图已生成并保存。
用 Finder 打开：open "$BRAND_WRITER_HOME/articles/<名>/images/"
```

## 健壮性

脚本对每张图做 3 次指数退避重试（间隔 2s/4s/8s）：
- HTTP 429/500/502/503/504 → 自动重试
- 网络超时 / JSON 解析错误 → 自动重试
- 4xx（非 429）→ 直接失败（prompt 本身有问题，比如违反 OpenAI 内容政策）
- 每张图成功**立即落盘**，不等其他图

失败不阻塞整批生成。最后汇总告诉用户：
> ✅ 成功 3/4，失败 1 张：cover.png (429 限流，已重试 3 次)
> 要重新生成失败的那张吗？

## 重新生成

用户可能说的命令：
- `重新生成第 N 张` → 只重新生成对应编号的图片，覆盖原文件
- `重新生成封面图` → 只重新生成 cover.png（含 sips crop）
- `换 prompt 重新生成` → 让用户给新 prompt，重新生成

## 环境变量

API Key 从环境变量 `OPENAI_API_KEY` 读取。如果未设置，告知用户：

> ⚠️ 未检测到 OPENAI_API_KEY 环境变量。
> 请在 `~/.zshrc` 中添加：`export OPENAI_API_KEY="你的 key"`
> 然后 `source ~/.zshrc` 后重试。

⚠️ macOS Python（python.org / Homebrew 安装版）若遇 SSL 证书错误，需要 `SSL_CERT_FILE` 指向 certifi 路径。脚本调用统一加：
```bash
SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
```

## 历史背景：为什么从 fal 切到 OpenAI

V1 用 fal.ai Recraft V3 在品牌封面场景遇到稳定性问题：
- 背景色 mode A/B 切换不可控（lottery）
- limited palette 颜色经常颠倒
- prompt 长度 ~1000 chars 硬限
- style 参数不稳（`hand_drawn` 直接 override 颜色）

OpenAI gpt-image-1 在同 prompt 下一次成功，稳定可靠。性能差异显著。

## 参考

- 封面图固定模板：`references/cover-template.md`（V4 重写为 V7-style 7 段，2026-05-08）
- Python 脚本：`scripts/generate_image_openai.py`（Path B 直调；Path A 不用脚本）
- ⚠️ `references/style-options.md` 已 deprecated（fal 时代的 6 种 style 在 OpenAI 不存在），保留作为历史参考
