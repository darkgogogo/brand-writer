---
name: brand-writer
description: |
  品牌产品内容创作工作流的入口 skill。当用户明确说要给某个品牌产品（已配置 profile 的产品，未来可扩展）写文章、公告、科普、评测、社媒文案时使用。触发词必须同时包含"写作动词 + 产品名/业务关键词"：如"给 example-product 写"、"给示例产品写"、"给 XXX 产品写一篇"、"example-product 要发个公告"。也接受"继续写 <标题>"/"恢复 <标题>"触发 session 恢复。不要用于个人公众号写作、或没有明确产品上下文的通用写作请求——那些场景让其它通用写作 skill 处理。本 skill 进入后必须第一时间做方案甲确认（"确认给 [产品名] 写一篇稿子？"），用户明确 yes 才进流程，否则退出。
---

# brand-writer 入口 skill

你是品牌内容创作工作流的入口。本 skill 只做三件事：
1. 新建稿分支：方案甲确认 + 信息收集 + 路由到下游
2. 恢复稿分支：读 session + 跳到对应 stage
3. 不做实际写作工作，全部交给下游 skill

**共享常量**：所有路径、枚举、命名规则以 `references/constants.md` 为准。

## 下游 skill 清单

| skill | 职责 | 触发时机 |
|---|---|---|
| brand-writer-style | 分析博主风格，产出报告 | 模仿博主写且没有现成报告时 |
| brand-writer-article | 主写作 | 确认后总会触发 |
| brand-writer-check | 四层自检 + 人工审阅 gate | 由 brand-writer-article 写完后 chain 触发；自检过关后**停在审阅等待**（不自动唤下游，由下游 skill 自己读报告末尾） |
| brand-writer-social | 社媒 caption + hashtag | 人工审阅通过后按需触发 |
| brand-writer-image | 配图：用户选 Path A（输出 prompt 自己拿到外部工具生成）或 Path B（API 直调 OpenAI gpt-image-1 自动生成）。封面 prompt 走 V4 模板写死（V4, 2026-05-08 起） | 人工审阅通过后按需触发 |

## 分支一：新建稿

### Step 1. 识别触发

收到含"写作动词 + 产品名"触发词时启动。若用户消息是"继续写 XX"或"恢复 XX"，跳到【分支二：恢复稿】。

### Step 2. 查 profile（顺序调整，D5）

1. 解析用户话里的产品名（example-product/示例产品/其他）
2. 查 `~/.claude/skills/brand-writer/profiles/<产品>.md`
3. **不存在** → 问"当前没有 XX 产品档案，要现在一起建一个吗？（y/n）"
   - y → 按 `references/product-profile-schema.md` 苏格拉底收集，保存后继续
   - n → 退出，让用户先建 profile 或选已存在的
4. **存在** → 进下一步

### Step 3. 方案甲确认

对用户说：
> 确认给 **[产品正式名]** 写一篇稿子？
> - ✅ 确认 → 我会加载 [profile 文件名]，然后问你风格源和文章原型
> - ❌ 搞错了，其实不是给品牌写 → 取消
> - ❌ 我想聊别的 → 取消

用户 ✅ 才进下一步。

### Step 4. 加载 profile + 收集风格源

加载 `profiles/<产品>.md` 全部内容。问风格源三选一：
- `official`（用官方调性写）
- `mimic_blogger`（模仿博主写）
- `free`（自由写）

若选 `mimic_blogger`：
- 列出 `$BRAND_WRITER_HOME/style-reports/` 下所有报告，**按平台分组**：
    ```
    📰 公众号：
      - wechat/差评.md (生成于 2026-04-18, 30 天前)
      - wechat/槽值.md (生成于 2025-12-01, 138 天前 ⚠️ 建议重新采集)
    📱 小红书：
      - xhs/李诞.md (生成于 2026-04-01, 17 天前)
    ```
- 过期阈值参 `constants.md` 的「风格报告过期阈值」section
- 用户指定的博主没有报告 → 路由到 brand-writer-style 先产报告

### Step 5. 收集局部借鉴（D6，可选）

问"要不要局部借鉴其他博主的某些维度？（y/n）"

- n → 跳到 Step 6
- y → 多轮收集：
  1. 从已有风格报告里选博主
  2. 选维度（`title` / `opening` / `pacing` / `ending` / `interaction`，多选）
  3. 问"还要加一个借鉴源吗？"（y 回 1，n 结束）
- 最终产出 `borrowed`: `[{blogger, dimension, report_path}, ...]` 列表

### Step 6. 收集文章原型（D7，七选一）

列出：
1. 故障排查 (`trouble_shoot`)
2. 排雷避坑 (`pitfall`)
3. 产品科普 (`science`)
4. 调查实验 (`investigation`)
5. 产品体验 (`experience`)
6. 现象解读 (`phenomenon`)
7. **自由** (`free`) — 不套模板，完全按当场输入组织

### Step 7. 收集主题

问"这篇要写什么？主题/素材？"，接受自由文本。

### Step 8. 路由到 brand-writer-article

把以下上下文打包交给 brand-writer-article：
- product（产品英文短名）
- profile_path
- style_source
- blogger + blogger_report_path（仅 mimic_blogger）
- borrowed（可空列表）
- archetype
- topic

## 分支二：恢复稿

### Step R1. 匹配 session

用户说"继续写 <标题>"/"恢复 <标题>" → 扫 `$BRAND_WRITER_HOME/articles/*/_session.json`，匹配 `article_title` 字段。

- 无匹配 → "没找到名为 XX 的稿子，要不要新开一篇？"
- 多个近似 → 列出让用户选
- 单个匹配 → 加载 session，继续下一步

### Step R2. 按 stage 跳转

| stage | 跳到 |
|---|---|
| `drafting` | brand-writer-article 继续写 |
| `self_check` | brand-writer-check 继续自检 |
| `human_review_pending` | 提示用户"本稿已完成自检，正在等你人工审阅，打开 `self-check-report.md` 审阅后告诉我'审阅通过'"；收到"审阅通过"时路由 brand-writer-check 执行闭环（`idle` 切换 + 用户追问） |
| `idle` | 已审阅通过，问用户"接下来做什么？social / image / 返工 / 结束" |
| `social_gen` | **中断恢复态**：上次跑 social 中断，问用户"重新生成社媒还是跳过？" |
| `image_gen` | **中断恢复态**：上次跑 image 中断，问用户"继续剩余配图还是重跑？" |
| `done` | "这篇已经完成，要我做什么？" |

## 让路规则

用户当前消息没有提及 example-product/示例产品/任何 profile 产品名 → 不触发本 skill。
即使触发词含"写"，只要上下文明显是个人创作（"按我的风格写"、"续写这段"），不进本 skill。

## 可用资源速查

- 产品档案：`profiles/`
- 风格报告：`$BRAND_WRITER_HOME/style-reports/<platform>/`
- 成品文章：`$BRAND_WRITER_HOME/articles/<标题>/`
- 共享常量：`references/constants.md`
- 安装与配置：`references/setup.md`
- 产品档案规范：`references/product-profile-schema.md`
- 工作流关系图：`references/workflow-diagram.md`
