# brand-writer Setup

Three optional steps to get going. The plugin works out of the box with default settings; everything below is for customization.

## Prerequisites

- Claude Code installed (CLI / desktop / IDE extension all work)
- Plugin installed: `/plugin install brand-writer` (or manual clone — see README)

## Step 1: (optional) Configure work directory

By default, articles and style reports are stored in `~/Documents/brand-writer/`. To change the location:

```bash
export BRAND_WRITER_HOME="$HOME/my-content"
mkdir -p "$BRAND_WRITER_HOME"/{articles,style-reports,_design}
```

Add the `export` line to your `~/.zshrc` or `~/.bashrc` to persist across shells.

**Obsidian users**: see `docs/obsidian-mode.md` in the plugin repo for vault setup.

## Step 2: (optional) Configure image generation

The `brand-writer-image` skill calls fal.ai for cover and inline images. To enable:

```bash
export FAL_API_KEY="fal_xxxxxxxxxxxxxxxxxxxx"
```

Get a key at https://fal.ai/dashboard/keys. Without this variable, the image skill will refuse to run with a clear error message.

## Step 3: (optional) Verify Python script is executable

```bash
chmod +x ~/.claude/plugins/brand-writer/skills/brand-writer-image/scripts/generate_image.py
python3 ~/.claude/plugins/brand-writer/skills/brand-writer-image/scripts/generate_image.py --help
```

Expected: argparse help output. Skip this step until you actually try to generate images.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `BRAND_WRITER_HOME directory does not exist` | env var set but path missing | `mkdir -p "$BRAND_WRITER_HOME"` |
| `FAL_API_KEY not set` (from image skill) | env var missing | Set per Step 2 |
| `python3: command not found` | no Python | macOS: `xcode-select --install`. Linux: install via package manager. |
| `Permission denied` on `generate_image.py` | missing executable bit | `chmod +x` per Step 3 |
