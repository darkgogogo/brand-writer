# brand-writer · 协作规则

**本仓库是公开 MIT 项目**（`github.com/darkgogogo/brand-writer`）。

## 私有内容隔离（硬规则）

- **不要**读取、引用或硬编码任何用户私有 vault（`~/.kb/` 等）路径
- **不要**在文档 / skill / 代码 / 测试 fixture 里出现用户私有业务的内部数据、用户研究、未公开决策、私有命名空间或私有代号
- **不要**引入 absolute path 到用户 home（`~/...`、`/Users/...`）；使用环境变量 `$BRAND_WRITER_HOME` 或相对路径
- 测试样本放 `./tests/fixtures/` 或 `./examples/`；用编造的占位品牌名（`example-brand` / `acme`）

> 注：letsvpn / 快连VPN 在 README 里作为 brand-writer 的应用场景示例已公开，可继续引用；但所涉品牌的内部数据、用户分群、运营策略等仍属私有。

## 公开范围

仓库公开 = skills / docs / scripts 全部可读。提交前自检：

- 没有真实业务内部数据 / 真实 API key / 真实 endpoint
- README 截图不含私有 vault 内容
- skill 描述里没有用户私有命名空间或代号

## 私有实例隔离

用户的私有工作流实例住在用户 KB 内，与本仓库通过 fork / 用户侧配置分离。**不在本 repo 内合并任何私有实例代码**。
