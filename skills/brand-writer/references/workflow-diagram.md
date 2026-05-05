# brand-writer 工作流关系图

## 典型调用链

```
用户触发（含产品名关键词）
  ↓
brand-writer（入口）
  → 方案甲确认
  → 加载 profile
  → 问风格源 + 原型
  ↓
[如选"模仿博主"且无现成报告]
  → brand-writer-style
  → 产出 style-report 到 KB
  ↓
brand-writer-article（主写作）
  → 苏格拉底提问收集信息
  → HKR 选题质检
  → 从业者素材收集（4 维度 + 原型门槛）
  → 写正文+标题+简介+关键词+封面 prompt（中英双语）
  → 写入 KB articles/<名>/<名>.md
  → 自动 chain 到 brand-writer-check
  ↓
brand-writer-check（自检）
  → L1 硬性规则扫描（按风格源选禁用词等级）
  → L2 风格一致性
  → L3 内容质量
  → L4 目标对齐 + 活人感
  → 产出独立的 self-check-report.md（与正文同目录）
  → 全通过后 stage=human_review_pending，等用户"审阅通过"
  ↓
[用户审阅通过后按需触发]
brand-writer-social → 社媒 caption + hashtag（中英，启动前校验人工审阅标记）
brand-writer-image → fal.ai 生成封面和正文配图
```

## 各 skill 的独立触发

除了 brand-writer 入口路由外，每个 skill 也可单独触发：

- `分析 XX 博主风格` → brand-writer-style
- `跑下自检`（带文章路径）→ brand-writer-check
- `给这篇文章写个微博` → brand-writer-social
- `生成配图` → brand-writer-image
- `开始创作`（已在会话中确认了产品）→ brand-writer-article

## 数据流

| 数据 | 来源 | 去处 |
|---|---|---|
| 产品档案（profile） | 预先存在 `~/.claude/skills/brand-writer/profiles/` | brand-writer 启动时读入上下文 |
| 博主风格报告 | brand-writer-style 产出 | 写入 KB `style-reports/`，brand-writer-article 引用 |
| 文章正文 | brand-writer-article 产出 | 写入 KB `articles/<名>/<名>.md` |
| 自检报告 | brand-writer-check 产出 | 独立文件 `articles/<名>/self-check-report.md`（与正文同目录） |
| 社媒文案 | brand-writer-social 产出 | 追加到文章 .md 的「社媒文案」section |
| 配图 | brand-writer-image 产出 | 写入 KB `articles/<名>/images/` |
