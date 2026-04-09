# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tech Book Generator — a Python CLI tool that converts Markdown into professional, print-optimized HTML/PDF technical tutorials with Chinese-English bilingual support. Pure Python 3.8+ with no required external dependencies.

## Commands

```bash
# Generate HTML from markdown
python3 generator.py --title "标题" --author "作者" --input content.md

# Generate HTML + PDF (requires playwright)
python3 generator.py --title "标题" --author "作者" --input content.md --pdf

# With all options
python3 generator.py --title "标题" --author "作者" --subtitle "副标题" \
  --theme blue --keywords "关键词1 · 关键词2" --audience "目标读者" \
  --input content.md --output output.html --pdf

# Install optional PDF dependency
pip3 install playwright && playwright install chromium

# Generate demo
python3 generator.py --title "演示" --author "Demo" --input example-enhanced.md --output demo.html
```

## Architecture

Single-file application with two core files:

- **`generator.py`** — `TechBookGenerator` class handles the full pipeline:
  1. `parse_markdown()` — Extracts frontmatter metadata, Part/Section structure, and content from Markdown
  2. `render_content()` — Converts Markdown subsets to HTML (headers, bold, italic, code blocks with syntax highlighting, tables, blockquotes, file trees, flowcharts, links)
  3. `generate_toc()` / `generate_content_body()` — Builds TOC and section HTML
  4. `generate_html()` — Loads `template.html`, replaces placeholders (`{title}`, `{content_body}`, etc.), applies theme colors via regex on CSS custom properties
  5. `convert_to_pdf()` — Playwright-first PDF conversion, falls back to `html2pdf.sh` or browser print

- **`template.html`** — Complete HTML/CSS template with CSS custom properties for theming (6 themes: blue, orange, green, purple, red, dark), print-optimized layout using Van de Graaf canon, cover page, TOC, part/section headers, code blocks, callout boxes, file trees, tables

## Markdown Convention

Input files use a structured format:
- `---` frontmatter block with title/subtitle/author/version/keywords/audience
- `# Part N: 部分标题` for part divisions
- `## §01 章节标题` for numbered sections (subtitle auto-detected if next line is English text < 100 chars)
- Standard Markdown for content: bold, italic, code blocks, blockquotes, tables, links

## Key Patterns

- Theme system: `THEMES` dict maps theme names to color palettes; applied by regex-replacing CSS custom property values in the template
- Syntax highlighting is hand-rolled regex (no Pygments) — covers Python keywords, strings, numbers, comments
- No tests, no linting, no build system — run directly with `python3 generator.py`

## Known Issues

- TOC page numbers are section counters, not actual page numbers
- Blockquote regex only handles single-line blockquotes
- Frontmatter parsing treats any `key: value` line before the first Part header as metadata — avoid colons in content before the first `# Part`
