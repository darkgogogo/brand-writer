---
name: brand-writer-social
description: |
  为品牌文章生成社媒 caption 和 hashtag（中英双语）。通常在 brand-writer-article 产出正文后用户主动触发。输入：文章路径。输出：追加到文章 .md 的「社媒文案」section。不要用于写标题和简介（那是 brand-writer-article 的活），只做社媒传播用的短文案。v1.0 只做通用版，未来可扩展分平台（小红书/X/微博）差异化。
---

# brand-writer-social 社媒文案 skill

> 本 skill 依赖 `~/.claude/skills/brand-writer/references/constants.md` 的共享常量（路径规则）。

## 输入

- 文章路径（主 `<标题>.md`）
- **前提**：同目录 `self-check-report.md` 末尾必须有 `**人工审阅**：✅ 通过` 一行（V2 新增 gate，D13）

读入正文、标题候选、简介，提炼钩子写社媒。

## 流程

### Step 0: 人工审阅 gate 校验（V2 新增，D13）

Read `articles/<标题>/self-check-report.md`，检查末尾是否含 `**人工审阅**：✅ 通过`：
- **无** → 拒绝执行，回复用户：
  > ❌ 未检测到人工审阅通过标记。
  > 请先打开 `articles/<标题>/self-check-report.md` 审阅，确认无误后告诉我"审阅通过"，我再继续生成社媒。
- **有** → 进 Step 1

### Step 1 起主流程

1. 更新 `_session.json.stage` → `social_gen`（运行中标记，若中途崩溃可识别为"上次跑到一半"）
2. 读文章，提取核心钩子（反差 / 悬念 / 痛点共鸣）
3. 写中文 caption（150 字以内）
4. 写英文 caption（under 120 words）
5. 生成中文 hashtags（8-10 个）
6. 生成英文 hashtags（8-10 个，与中文相关但非直译）
7. 追加到主 `<标题>.md` 的「社媒文案」section（若已存在则整段覆盖——手改过的内容会丢，如需保留先复制走）
8. 成功收尾：更新 `_session.json.stage` → `idle`（等用户指派下一步：image / 结束 / 返工）

## 写作规范

### 中文 Caption
- 150 字以内
- emoji 密集穿插（每 1-2 句一个）
- 短句直接抓眼球
- 首句必须有钩子，不要摘要式
- 结尾附链接：`🔗 阅读全文：[文章链接]`

### 英文 Caption
- under 120 words
- emoji every 1-2 sentences
- punchy short sentences
- 不是中文直译，为英文读者重新构思钩子
- 结尾附链接：`🔗 Read the full article: [article link]`

### Hashtags

**中文**：8-10 个，品牌 + 主题 + 领域混合
示例：

```text
#FocusFlow #专注力 #知识工作 #深度工作 #生产力工具 #ChatGPT #远程办公
```

**英文**：8-10 个
示例：

```text
#FocusFlow #DeepWork #Productivity #FlowState #KnowledgeWork #FocusMode #RemoteWork
```

> ⚠️ **必须用 ` ```text ` code block 包裹**，避免 Obsidian 把 hashtag 解析为笔记 tag。

## 输出格式

**追加到主 `<标题>.md` 文件**，在文件末尾的「社媒文案」section（如已存在则覆盖）。**不**写入 `self-check-report.md`。

````markdown
## 社媒文案

### 中文
**Caption**
[150 字以内，emoji 每 1-2 句一个]
🔗 阅读全文：[文章链接]

**Hashtags**

```text
#FocusFlow #...
```

### English
**Caption**
[under 120 words, emojis every 1-2 sentences]
🔗 Read the full article: [article link]

**Hashtags**

```text
#FocusFlow #DeepWork #...
```
````

## 写好后告知用户

> ✅ 社媒文案已追加至 `$BRAND_WRITER_HOME/articles/<名>/<名>.md` 的「社媒文案」section。
> 中英 caption 各一版、hashtag 中英各 8-10 个。如需调整或分平台差异化，告诉我改哪里。

## 边界

- 只做通用社媒文案，不分平台（v1.0）
- 不改正文、标题、简介
- 未来扩展分平台见 references/platform-patterns.md
