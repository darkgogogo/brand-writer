# Changelog

## v0.3.0 (2026-05-11) - Broaden audience: de-VPN defaults + V4.1 cover-template + Path A spotlight

This release makes the plugin genuinely cross-industry by removing baked-in VPN flavor from defaults and giving every product profile the levers to define its own visual identity.

### Breaking (only visible if you customized the V4 cover-template literally)

- **Cover-template upgraded to V4.1** (`brand-writer-image/references/cover-template.md`). The 7-section structural skeleton is unchanged, but `laptop` / `circular checkmark badge` / `successful restoration` / palette colors are now `[MAIN_OBJECT]` / `[TOP_BADGE_SHAPE]` / `[TOP_BADGE_SEMANTIC]` / 5 color variables, sourced from each product profile's `## 封面默认值` section. If you wrote a custom V4 prompt that hardcoded `laptop`, it still works as-is — but the new variable approach is cleaner.
- **Default scaffold profile renamed** from `example-product.md` to `focusflow.md`. Anyone whose code paths referenced the file by literal name needs to update; the schema doc / README / SKILL.md trigger phrases all now reference `focusflow`.

### Added

- **Profile-level cover defaults**: every product profile can declare a `## 封面默认值` section with 11 fields (5 colors, 3 main-object fields, product icon, 2 top-badge fields). Cover prompts inherit these on every article; you only fill the per-article concept / headline / surrounding elements.
- **FocusFlow sample profile**: a fictional productivity SaaS replacing the previous VPN-flavored "example-product" scaffold. Demonstrates the full profile structure (positioning, target users, pain points, technical vocabulary, brand rules, cover defaults, etc.) for any non-VPN audience.
- **README Path A spotlight**: a 💡 callout at the top of "安装" / "Install" sections makes clear that **image generation works with no API key** by default — only opt-in OpenAI automation needs `OPENAI_API_KEY`. Lowers the entry bar for new users who just want to try the plugin.

### Changed

- **`article-archetypes.md` examples**: all 7 archetype typical-title examples rewritten from VPN-flavored (`为什么 VPN 开着 AI 反而用不了`, `我们花了 30 天测了 20 个 AI 节点`, etc.) to cross-industry (`番茄钟为什么总坚持不到第三个`, `我们用 5 款生产力工具同时跟踪了 30 天的注意力数据`, etc.). The archetype taxonomy / structure /素材门槛 are unchanged.
- **`brand-writer-article/SKILL.md`**: cover-prompt 填空变量 table now shows two layers (品牌级 inherit-from-profile vs 每篇必填), aligned with the V4.1 template.
- **`product-profile-schema.md`**: 3 example references updated from `example-product` to `focusflow`; filename convention rewords "必须连字符" → "小写、可用连字符".
- **`brand-writer-check/references/banned-words.md`**: `## 豁免词` example switched from `精准识别节点` (VPN term) to `深度专注模式` (FocusFlow term).
- **`brand-writer-social/SKILL.md`**: hashtag examples switched from VPN themes to productivity themes.
- **`constants.md`**: 目录名 examples rewritten to non-VPN titles.

### Not changed (audited and OK)

- `banned-words.md` 🔴/🟡/🟢 word lists — already brand-neutral (all generic AI-vapor terms).
- 7 archetype taxonomy itself — universal enough to apply to any product domain.
- All V4 (2026-05-08) Path A/B fork mechanics and prompt template structure.

### Migration notes

- If you have a custom product profile that copied the old VPN cover defaults: copy the `## 封面默认值` section template from `focusflow.md` and adapt your brand's colors / main object / badge to make covers properly branded.
- If your code referenced `profiles/example-product.md` by exact path: change to `profiles/focusflow.md`.

## v0.2.0 (2026-05-11) - Image-gen V3 + V4 sync

This release ports the upstream content workflow's V3 (2026-05-06) and V4 (2026-05-08) changes for image generation.

### Breaking

- **`brand-writer-image` switched image backend from fal.ai Recraft V3 to OpenAI `gpt-image-1`** (V3, 2026-05-06). The original `scripts/generate_image.py` (fal) is removed; the new `scripts/generate_image_openai.py` is the only backend.
- **Environment variable renamed**: `FAL_API_KEY` → `OPENAI_API_KEY`. Path A (external tool hand-off, new in V4) needs no key at all, so this only affects users on Path B.

### Added

- **Path A / Path B fork in `brand-writer-image`** (V4, 2026-05-08): on first image step per article, the skill asks once whether to use **Path A** (external tools — ChatGPT client / Midjourney / Figma — for cover-quality output, then paste absolute paths back to the skill) or **Path B** (API direct call to OpenAI `gpt-image-1`). Path A is recommended for branded covers; Path B is ideal for batch / icon-level / automation. The same prompt text is used for both paths.
- **V7-style 7-section cover-template** (`brand-writer-image/references/cover-template.md`, V4, 2026-05-08): replaces the V1 Subject-only template with a full Style / Main concept / Composition / Surrounding elements / Top center / Visual details / Restrictions structure. Default brand palette (`#EEEEFE` / deep navy / lavender / coral-orange) and `laptop` main object are configurable per product profile.
- **Resumption support for Path A interruptions**: `_session.json.image_path` field (`"external"` / `"api"`) records which path was chosen, so an interrupted Path A session can resume cleanly instead of falling back to Path B.
- **macOS `sips` auto-crop**: OpenAI doesn't support 16:9 sizes; the skill auto-crops from `1536x1024` (3:2) to `1536x864` (16:9) via the macOS-built-in `sips -c` utility. No external image-processing tools needed.

### Changed

- `brand-writer-article` now writes covers per the V4 7-section template (fills `[MAIN_CONCEPT]` / `[HEADLINE_*]` / `[SUBTITLE_EN]` / 3 surrounding elements / etc.) instead of the V1 Subject-only single line.
- `brand-writer-image/references/style-options.md` marked deprecated (kept as historical reference): the fal Recraft V3 6-style enum doesn't exist in OpenAI's API. Style descriptions now go directly into each prompt.
- README: install Step 3 / quick-start Step 5 / troubleshooting table / English section all updated to reference `OPENAI_API_KEY` and Path A/B.
- `brand-writer/references/setup.md`: rewritten to cover both paths, with cost reference for Path B quality tiers (~$0.17 / $0.04 / $0.01 per image at high / medium / low).

### Removed

- `brand-writer-image/scripts/generate_image.py` (fal backend).
- `FAL_API_KEY` references throughout the plugin.

### Notes

- Path B requires Python 3 + `certifi` package (`pip install --user certifi`) for SSL on macOS.
- ChatGPT-client output quality on cover prompts is observed to be noticeably better than direct OpenAI API on the same model (the client appears to apply an implicit prompt enhancer / smart-size / N-best retry). Hence Path A is recommended for branded covers.

## v0.1.0 (2026-05-05) - Initial public release

- 6 skills: brand-writer (entry), brand-writer-article, brand-writer-style, brand-writer-social, brand-writer-image, brand-writer-check
- Dual-mode storage: default `~/Documents/brand-writer/` or `BRAND_WRITER_HOME` env var (e.g. point to an Obsidian vault)
- `example-product` profile included as scaffold
