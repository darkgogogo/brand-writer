# Obsidian Mode

`brand-writer` works fine on plain folders, but if you already use Obsidian, pointing `BRAND_WRITER_HOME` at a vault folder gives you wiki-links, Dataview queries, and Canvas integration for free.

## Setup

```bash
export BRAND_WRITER_HOME="$HOME/Obsidian/MyVault/AI Writer"
mkdir -p "$BRAND_WRITER_HOME"/{articles,style-reports,_design}
```

Persist by adding to `~/.zshrc` or `~/.bashrc`.

## What you get for free

### Wiki links between articles

Every article folder is a regular Obsidian note. Link articles with `[[article-name]]`.

### Dataview: list all articles by month

```dataview
TABLE created, status
FROM "AI Writer/articles"
WHERE file.name = "index" OR file.name = file.folder
SORT created DESC
```

### Dataview: filter by product

```dataview
TABLE created
FROM "AI Writer/articles"
WHERE contains(string(file.path), "your-product")
SORT created DESC
```

### Canvas: visualize article relationships

Drop article folders onto a `.canvas` to see relationships — works because each article is markdown.

## Tips

- Don't edit `_session.json` in Obsidian — it's the resume-state file for skills
- Style reports under `style-reports/<platform>/` are normal markdown — feel free to backlink them from articles
- The plugin's `profiles/` directory stays in `~/.claude/plugins/brand-writer/skills/brand-writer/profiles/`, NOT in your vault. Keep it that way — profiles are plugin config, not user data.
