---
name: brand-writer-style
description: |
  分析外部博主的写作风格，产出结构化风格报告存到 Obsidian KB。当用户说"分析 XX 博主风格"、"研究一下 XX 的文风"、"帮我扒下 XX 的风格"时触发。也被 brand-writer 在用户选择"模仿博主写"但无现成报告时路由调用。不要用于生成文章正文（那是 brand-writer-article 的活），只做风格分析和报告生成。
---

# brand-writer-style

对指定博主做风格分析，产出可被 brand-writer-article 作为"模仿博主写"风格源引用的报告。

> 本 skill 依赖 `~/.claude/skills/brand-writer/references/constants.md` 的共享常量定义，所有路径、枚举（尤其平台 `wechat/xhs/x/weibo/crossplatform`）、命名规则以那里为准。

## 工作流程

### 1. 检查是否已有报告
```bash
ls $BRAND_WRITER_HOME/style-reports/
```

- 有该博主报告 → 询问用户是否直接复用；确认则退出本 skill
- 没有 → 进入分析流程

### 2. 苏格拉底式信息收集

每次只问一个问题，按顺序：
1. 博主主要活跃平台（微信公众号 / X / 微博 / 抖音 / YouTube / 小红书 / 知乎 / B站 / Medium / LinkedIn / 头条 / 百家号 / 博客域名）
2. **主阵地归档平台**（`wechat` / `xhs` / `x` / `weibo` / `crossplatform`）——决定报告落盘子目录。若博主跨平台发但重心不明确，选 `crossplatform`。
3. 是否允许联网抓取（某些博主可能需要手动提供内容，尤其公众号）
4. 是否有手动提供的素材（公众号文章链接、粘贴的原文等）
5. 语气基调偏好（你期待复制博主的风格程度：严格还原 / 保留核心风格但品牌化）
6. 是否多篇联动（如果是系列报告，影响分析深度和维度）

把握到 95% 后主动告知"已充分了解，开始分析"，进入下一步。

### 3. 内容搜集

目标：**8-15 篇，优先最近 3 个月**。

| 渠道 | 搜索策略 |
|---|---|
| 微信公众号 | `{博主名} site:mp.weixin.qq.com`；通常需用户手动提供 |
| 私人博客 | 直接访问域名；或 `{博主名} blog 博客` |
| X/Twitter | `x.com/{用户名}`；`from:{用户名}` 找近期推文 |
| 微博 | `{博主名} site:weibo.com` |
| 抖音 | 搜博主账号；置顶脚本；字幕转录 |
| YouTube | 频道页；5分钟以上讲解视频；字幕/转录 |
| 小红书 | `{博主名} site:xiaohongshu.com` |
| 知乎 | `{博主名} site:zhihu.com` |
| B站 | UP主频道；视频简介；口播转录 |
| Medium | `{博主名} site:medium.com` |
| LinkedIn | 博主主页；长文和动态 |
| 头条号/百家号 | `{博主名} site:toutiao.com` 或 `baijiahao.baidu.com` |

不足 5 篇时主动告知用户，说明分析置信度有限。

### 4. 按五维度分析

五个维度（详见 references/style-report-template.md）：
- 基础表达层：选题偏好 / 标题风格 / 开篇方式 / 结尾习惯
- 叙事结构层：行文节奏 / 论证方式 / 过渡设计 / 悬念与钩子 / **文化升维倾向**（none/low/mid/high，决定 brand-writer-check L3-3 是否对模仿该博主的稿件启用文化升维检查）
- 语气人设层：整体语气 / 人称习惯 / 专属表达 / 情绪曲线
- 读者互动层：互动设计 / 共情策略 / 金句密度
- 媒介适配层：排版特征 / 素材偏好 / 篇幅规律 / 平台差异

### 5. 产出报告

写入路径：`$BRAND_WRITER_HOME/style-reports/<platform>/<博主名>.md`

若对应 `<platform>` 子目录不存在，先 `mkdir -p` 再写入。

**必含以下 9 个 section**：
1. 五个分析维度（基础表达 / 叙事结构 / 语气人设 / 读者互动 / 媒介适配）
2. 核心风格关键词（3-5 个）
3. **推荐词组清单**（该博主高频口语化表达，8-15 个，写作时主动用）
4. **禁用词清单**（该博主绝不会说的 AI 味词，5-10 个，brand-writer-check 会读取）
5. **专属自称**（博主特有自称如「差评君」，brand-writer 写作一律禁用）
6. 最具代表性的表达习惯（2-3 个具体例子，含原文片段）

模板详见 references/style-report-template.md。

### 6. 保存后告知用户

> ✅ **风格报告已生成并保存至** `$BRAND_WRITER_HOME/style-reports/<platform>/<博主名>.md`
>
> 下次给品牌产品写稿时选择"模仿博主写" → 选 [博主名]，即可直接使用本报告。

## 边界

- **只分析，不创作**：不输出文章正文，只输出风格报告。
- **换博主必须重新执行**：风格报告不跨博主复用。
- **报告是活的**：用户可随时让你追加/修正某个维度。
