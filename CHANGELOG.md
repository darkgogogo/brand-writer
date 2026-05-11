# Changelog

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
