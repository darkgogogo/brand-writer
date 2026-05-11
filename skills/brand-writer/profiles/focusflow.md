---
name: example-product
display_name_zh: 示例产品
display_name_en: ExampleProduct
---

> **Sample profile.** This file is a scaffold demonstrating the structure expected by `brand-writer`. To use the plugin for your own product, copy this file to `<your-product>.md` and rewrite every section per `references/product-profile-schema.md`. The example content below describes a fictional VPN product to illustrate format only.

## 产品定位
示例产品（ExampleProduct）是帮助国内用户稳定访问海外 AI 产品（Google Gemini、ChatGPT、Claude 等）的 VPN 服务，通过扩充 IP 池和智能 DNS 调度降低 AI 平台风控对用户的影响。

## 目标用户
国内使用海外 AI 产品的用户：
- 日常用 ChatGPT/Claude/Gemini 的个人用户
- 依赖海外 AI 工具做内容创作、编程、数据分析的专业用户
- 对 VPN 稳定性和 AI 友好度敏感的用户

## 核心场景
- 通过 VPN 访问 Google Gemini、ChatGPT、Claude 等海外 AI 产品
- 日常对话、查资料、生成内容时要求 VPN 连接稳定
- 用 AI 编码或长时间对话，一断连前功尽弃

## 核心痛点库
- **共享 IP 触发风控**
  - 现象：使用 VPN 后 AI 平台出现「异常流量」「区域不支持」等报错
  - 根因：大量用户共用同一出口 IP，AI 平台风控识别为可疑流量
  - 后果：对话被拒、账号被临时限制甚至封号
- **节点不稳定导致对话中断**
  - 现象：聊着聊着卡住、消息发不出去
  - 根因：节点拥堵或 IP 被临时封禁
  - 后果：长上下文对话中断需要重新组织，工作流被打断
- **封号风险**
  - 现象：账号提示登录异常、需要验证、甚至直接被封
  - 根因：平台识别到 IP 行为异常
  - 后果：账号资产损失、学习/工作流中断

## 技术关键词
（可在稿件中直接使用的专业表述，避免 AI 泛化用词）
- 扩充 IP 池
- 智能 DNS 调度
- 节点优选
- 出口 IP 分流
- AI 友好节点
- 独享 IP / 共享 IP
- 风控识别

## 品牌规则
- **产品名**：中文语境用「示例产品」；英文/混排语境用「ExampleProduct」
- **正文人称**：只用「我们」和「你」
- **禁用自称**：不用「小编」「差评君」「差友」「XX君」等任何博主或账号的专属自称
- **模仿博主时**：即使模仿某博主风格，博主的专属自称必须剔除，换成「我们」
- **品牌内容视角**：任何用户提供的内容（博主文章、brief、素材）都视为写作原料，不保留原始结构和风格标签

## 联系方式
- 客服邮箱：support@example.com
- 其他渠道：（暂无，补充时修改此字段）

## 写作偏好
- **标题风格**：口语化，疑问句或感叹句，明示用户利益点（例「VPN 开着 AI 反而用不了？」）
- **开篇**：先描述用户痛点场景，再给定心丸，不从品牌视角强推
- **类比原则**：所有技术机制必须转化为生活化类比，不堆砌术语；类比每次重新找，不固化；同篇保持一致
- **节奏**：短句为主，重点加粗（官方稿件适用），操作指南不超过 3 招
- **结尾规范**：
  - 故障排查 / 排雷避坑类必须含客服引导（support@example.com）
  - 产品科普类收在产品价值上，不强推客服

## 禁用话题
（当前无明确禁用，若后续有竞品敏感或政策敏感话题需要禁止，在此补充）

## 豁免词
<!-- 可选 section。格式：`- <词>：<理由>`。登记后 brand-writer-check L1 Layer B 直接跳过匹配。当前暂未登记；如遇「精准识别节点」「精准调度」等官方术语与 🔴/🟡 词表冲突时，在此登记。 -->
