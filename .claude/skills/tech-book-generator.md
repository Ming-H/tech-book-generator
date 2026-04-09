---
name: tech-book-generator
description: 使用 Tech Book Generator 将 Markdown 转化为专业排版的技术教程 HTML/PDF。当用户要求"生成技术文档"、"生成教程PDF"、"生成技术书籍"、"制作技术教程"时触发。
argument-hint: [markdown文件路径] [选项]
user-invocable: true
allowed-tools: Bash(python3*generator.py*), Bash(open*), Bash(pip3*), Bash(playwright*), Read, Write
---

# Tech Book Generator Skill

将 Markdown 内容生成专业排版的技术教程 HTML 或 PDF。

## 触发条件

当用户要求以下操作时触发：
- "生成技术文档/教程/书籍"
- "把 Markdown 转成 PDF"
- "制作技术教程"
- "用 Tech Book Generator 生成"

## 项目位置

`/Users/z/Documents/work/tech-book-generator/`

## 执行步骤

### 1. 确认输入

- 如果用户提供了 Markdown 文件路径，使用该文件
- 如果没有提供，询问用户提供输入文件路径，或使用项目中的示例文件 `example-enhanced.md`

### 2. 确认选项

询问或根据用户需求选择：
- `--title`：标题（必需，默认从 frontmatter 读取）
- `--author`：作者（必需，默认从 frontmatter 读取）
- `--theme`：主题配色（blue/orange/green/purple/red/dark，默认 blue）
- `--pdf`：是否同时生成 PDF
- `--output`：输出文件路径

### 3. 执行生成

在工作目录 `/Users/z/Documents/work/tech-book-generator/` 下执行：

```bash
cd /Users/z/Documents/work/tech-book-generator && python3 generator.py --input <输入文件> --output <输出路径> [其他选项]
```

常用命令模板：

```bash
# 仅生成 HTML
python3 generator.py --title "标题" --author "作者" --input content.md --output output.html

# 生成 HTML + PDF
python3 generator.py --title "标题" --author "作者" --input content.md --output output.html --pdf

# 使用指定主题
python3 generator.py --title "标题" --author "作者" --input content.md --theme green --output output.html
```

### 4. 展示结果

- 生成完成后，使用 `open` 命令在浏览器中打开 HTML 文件
- 如果生成了 PDF，告知用户 PDF 文件路径

## 注意事项

- Playwright 未安装时，PDF 生成会失败。安装命令：`pip3 install playwright && playwright install chromium`
- 输出到 `/tmp/` 目录的文件重启后会丢失，如需保存应输出到项目目录或其他持久化位置
