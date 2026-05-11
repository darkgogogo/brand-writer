# brand-writer Setup

Three optional steps to get going. The plugin works out of the box with default settings; everything below is for customization.

## Prerequisites

- Claude Code installed (CLI / desktop / IDE extension all work)
- Plugin installed: `/plugin install brand-writer` (or manual clone — see README)
- Python 3 (for image-generation Path B — pre-installed on macOS / available via package manager on Linux)
- `certifi` Python package (for image-generation Path B SSL):
  ```bash
  python3 -m pip install --user certifi
  ```

## Step 1: (optional) Configure work directory

By default, articles and style reports are stored in `~/Documents/brand-writer/`. To change the location:

```bash
export BRAND_WRITER_HOME="$HOME/my-content"
mkdir -p "$BRAND_WRITER_HOME"/{articles,style-reports,_design}
```

Add the `export` line to your `~/.zshrc` or `~/.bashrc` to persist across shells.

**Obsidian users**: see `docs/obsidian-mode.md` in the plugin repo for vault setup.

## Step 2: (optional) Configure image generation

The `brand-writer-image` skill supports two paths (V4, 2026-05-08):

- **Path A (recommended)**: skill outputs prompts → you generate via external tools (ChatGPT client / Midjourney / Figma) → paste absolute paths back. **No API key needed.**
- **Path B (automated)**: skill calls OpenAI `gpt-image-1` directly. Needs `OPENAI_API_KEY`:

  ```bash
  export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxx"
  ```

  Get a key at https://platform.openai.com/api-keys. Without this variable, Path B will refuse to run with a clear error; Path A still works fine.

Cost reference (Path B, OpenAI gpt-image-1):
- `quality=high` (default, recommended for cover): ~$0.17 / image
- `quality=medium`: ~$0.04 / image
- `quality=low`: ~$0.01 / image

## Step 3: (optional) Verify Python script is executable

Only needed if you plan to use Path B:

```bash
chmod +x ~/.claude/plugins/brand-writer/skills/brand-writer-image/scripts/generate_image_openai.py
python3 ~/.claude/plugins/brand-writer/skills/brand-writer-image/scripts/generate_image_openai.py --help
```

Expected: argparse help output. Skip this step until you actually try to generate images via Path B.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `BRAND_WRITER_HOME directory does not exist` | env var set but path missing | `mkdir -p "$BRAND_WRITER_HOME"` |
| `OPENAI_API_KEY not set` (from image skill Path B) | env var missing | Set per Step 2 |
| `SSL: CERTIFICATE_VERIFY_FAILED` on Path B call | macOS Python missing CA bundle | Run script with `SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") python3 ...` (the skill already wraps calls this way) |
| `python3: command not found` | no Python | macOS: `xcode-select --install`. Linux: install via package manager. |
| `Permission denied` on `generate_image_openai.py` | missing executable bit | `chmod +x` per Step 3 |
| OpenAI 16:9 cover looks off | `gpt-image-1` only generates 3:2 / 1:1 / 2:3 | The skill auto-crops via `sips -c 864 1536` (macOS-only) to 16:9 |
