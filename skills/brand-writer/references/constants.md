# Brand Writer 共享常量

> 所有 brand-writer-* skill 依赖本文件定义的路径、枚举和命名规则。修改本文件会影响 6 个 skill 的行为，改动前先确认下游兼容。

## 工作目录解析（BRAND_WRITER_HOME）

所有 skill 都通过环境变量 `BRAND_WRITER_HOME` 定位文章/风格报告/设计文档的存放目录。

**解析规则：**

1. 若 `BRAND_WRITER_HOME` 已设置 → 使用该路径（支持 `~` 展开和绝对路径）
2. 若未设置 → 默认 `~/Documents/brand-writer/`
3. Skill 启动时验证目录存在；不存在则报错并提示用户手动 `mkdir -p $BRAND_WRITER_HOME/{articles,style-reports,_design}`

**两种典型用法：**

```bash
# 普通模式（零配置）
# 不用设环境变量，文件存到 ~/Documents/brand-writer/

# Obsidian 模式
export BRAND_WRITER_HOME="$HOME/Obsidian/MyVault/AI Writer"
# 自动获得 wiki-link / dataview 能力
```

**Profile 路径例外**：`profiles/` 永远在 plugin skill 目录里（`~/.claude/skills/brand-writer/profiles/`），不受 `BRAND_WRITER_HOME` 影响。profile 是 plugin 内置配置，不是用户产出物。

## 工作目录布局

- 工作目录根：`$BRAND_WRITER_HOME/`（默认 `~/Documents/brand-writer/`）
- 文章：`$BRAND_WRITER_HOME/articles/`
- 风格报告：`$BRAND_WRITER_HOME/style-reports/<platform>/`
- 设计文档：`$BRAND_WRITER_HOME/_design/`

## 文章目录结构

```
articles/<标题>/
├── <标题>.md              # 正文 + 英文版 + 社媒文案
├── self-check-report.md   # 4 层自检 + 人工审阅状态（独立）
├── _session.json          # 会话恢复状态
└── images/
    ├── cover.png
    └── img1.png ... imgN.png
```

## 命名规则

### 文章目录名
基于文章主标题按以下顺序清洗（顺序很重要）：
1. 连续空格 → 单个连字符 `-`（先于第 3 步执行，避免空格被删）
2. 删除所有标点符号：`? ！ 。 ， ：； "" '' （）《》 ?!.,:;'"()<>` 及换行符
3. 只保留中文字符、英文字母、数字、连字符 `-`
4. 结果首尾去连字符

**示例**：
- 标题「VPN 开着 AI 反而用不了？」→ 目录名 `VPN-开着-AI-反而用不了`
- 标题「我花了 30 天测了 20 个节点」→ 目录名 `我花了-30-天测了-20-个节点`
- 标题「示例产品 的 AI 友好节点是什么」→ 目录名 `示例产品-的-AI-友好节点是什么`

### 其他
- Profile：`<产品英文短名>.md`，小写，连字符（例：`example-product.md`）
- 风格报告：`<platform>/<博主名>.md`（例：`wechat/差评.md`）

## 配图标注格式（单源）

**精确格式**（所有 brand-writer-* skill 共用）：

```
📷 **配图建议**（AI生成/设计师制作）：<30-50 字中文画面描述>
```

**组成要求**：
- 前缀：`📷 **配图建议**`（emoji + 加粗标签）
- 后缀：`（AI生成/设计师制作）`（全角括号，斜杠分隔）
- 冒号：全角 `：`
- 描述：30-50 字中文，主体 + 场景 + 情绪/构图三要素；不写风格词、不写颜色词

本 section 是单一事实来源——write-article 写稿、self-check Layer C 扫描、generate-images 解析都以此为准。

## 风格源枚举

| 值 | 含义 |
|---|---|
| `official` | 用官方调性写（产品档案里的品牌调性） |
| `mimic_blogger` | 模仿博主写（需风格报告） |
| `free` | 自由写（无固定风格） |

## 借鉴维度枚举

| 值 | 含义 |
|---|---|
| `title` | 标题套路 |
| `opening` | 开篇钩子 |
| `pacing` | 叙事节奏 |
| `ending` | 结尾 |
| `interaction` | 互动设计（提问 / 共情 / 金句） |

## 文章原型枚举

| 值 | 中文名 |
|---|---|
| `trouble_shoot` | 故障排查 |
| `pitfall` | 排雷避坑 |
| `science` | 产品科普 |
| `investigation` | 调查实验 |
| `experience` | 产品体验 |
| `phenomenon` | 现象解读 |
| `free` | 自由（不套模板） |

## Stage 枚举（_session.json）

| 值 | 含义 | 谁写入 |
|---|---|---|
| `drafting` | 正在写正文 | brand-writer-article（开写时） |
| `self_check` | 正文已落稿，自检中 | brand-writer-article（写完，chain 前） |
| `human_review_pending` | 自检过关，等人工审阅 | brand-writer-check（4 层全过后） |
| `idle` | 已审阅，等用户指派下一步（social / image / 返工 / 结束） | brand-writer-check（用户说"审阅通过"时） |
| `social_gen` | **运行中**：正在生成社媒（中断恢复标记） | brand-writer-social（开跑时） |
| `image_gen` | **运行中**：正在生成配图（中断恢复标记） | brand-writer-image（开跑时） |
| `done` | 全流程完成 | brand-writer-social / brand-writer-image（成功收尾时） |

**语义约定**：`social_gen` / `image_gen` 是**进行时**，完成后必须切回 `idle`（或若用户明示结束则 `done`）。稿子重新打开时停在 `social_gen` / `image_gen` 表示"上次跑到一半中断"，恢复流程要问用户"继续还是重跑"。

## 平台枚举（风格报告）

| 值 | 平台 |
|---|---|
| `wechat` | 公众号 |
| `xhs` | 小红书 |
| `x` | X / Twitter |
| `weibo` | 微博 |
| `crossplatform` | 跨平台或难归类 |

## 风格报告过期阈值

- `<90 天`：正常
- `90-180 天`：⚠️ 显示"N 天前"警告
- `>180 天`：🔴 强提示"博主调性可能已迁移，建议重新采集"
