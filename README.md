# Tech Book Generator

专业技术文档生成器，将 Markdown 转化为专业排版的 HTML/PDF 技术教程，支持中英双语和多主题配色。

## 功能特点

- 专业技术教程风格排版（Van de Graaf 黄金比例边距）
- 6 种主题配色：科技蓝、经典橙、翡翠绿、紫罗兰、玫瑰红、深海蓝
- 中英文双语标题支持
- 多语言代码语法高亮（Python、Bash、JS、CSS、HTML）
- 代码块语言标签显示
- GitHub Alerts 风格提示框（`[!NOTE]`、`[!TIP]`、`[!WARNING]`、`[!DANGER]`、`[!SUCCESS]`）
- 有序列表、无序列表、步骤编号
- 自动生成目录 (TOC)
- 打印优化（黄金比例边距、避免跨页分割）

## 安装

```bash
# 克隆仓库
git clone https://github.com/Ming-H/tech-book-generator.git
cd tech-book-generator

# 安装可选依赖（用于 PDF 转换）
pip3 install playwright
playwright install chromium
```

> 纯 Python 3.8+ 项目，无必需依赖。生成 HTML 无需安装任何第三方包。PDF 转换需要 Playwright。

## 使用方法

```bash
# 生成 HTML
python3 generator.py --title "标题" --author "作者" --input content.md

# 生成 HTML + PDF
python3 generator.py --title "标题" --author "作者" --input content.md --pdf

# 完整选项
python3 generator.py \
  --title "React 进阶指南" \
  --author "张三" \
  --subtitle "从入门到精通" \
  --theme green \
  --keywords "React · 前端 · JavaScript" \
  --audience "前端开发者" \
  --input content.md \
  --output output.html \
  --pdf

# 使用示例文件快速体验
python3 generator.py --title "演示" --author "Demo" --input example-enhanced.md --output demo.html
```

## 命令行参数

| 参数 | 说明 | 必需 |
|------|------|------|
| `--title` | 书籍标题 | 是 |
| `--author` | 作者名称 | 是 |
| `--input` / `-i` | 输入 Markdown 文件 | 是 |
| `--output` / `-o` | 输出 HTML 文件 | 否 |
| `--subtitle` | 副标题 | 否 |
| `--series` | 系列名称（默认：技术文档） | 否 |
| `--version` | 版本号 | 否 |
| `--keywords` | 关键词（用 · 分隔） | 否 |
| `--audience` | 目标读者 | 否 |
| `--theme` | 主题配色（默认：blue） | 否 |
| `--pdf` | 同时生成 PDF | 否 |
| `--template` / `-t` | 自定义 HTML 模板 | 否 |

## Markdown 格式

```markdown
---
title: 主标题
subtitle: 副标题
series: 技术文档
author: 作者名
version: v260409
keywords: 关键词1 · 关键词2
audience: 目标读者
---

# Part 1: 概念

## §01 章节标题
Section Subtitle

章节内容...

### 子标题

更多内容...

> [!TIP]
> 使用技巧提示框

> [!WARNING]
> 注意事项

| 特性 | 说明 |
|------|------|
| 功能1 | 描述1 |

```python
def example():
    return "Hello"
```
```

## 主题配色

| 主题 | 风格 | 推荐场景 |
|------|------|----------|
| `blue` | 科技蓝（默认） | 编程、AI、云技术 |
| `orange` | 经典橙 | 教程、入门指南 |
| `green` | 翡翠绿 | 长篇文档、实践指南 |
| `purple` | 紫罗兰 | 创新技术 |
| `red` | 玫瑰红 | 前端开发 |
| `dark` | 深海蓝 | 企业文档、架构设计 |

## 项目结构

```
tech-book-generator/
├── generator.py           # 主程序
├── template.html          # HTML 模板
├── example.md             # 基础示例
├── example-enhanced.md    # 完整示例
├── html2pdf.sh            # 浏览器打印脚本
└── LICENSE                # MIT 许可证
```

## 许可证

[MIT License](LICENSE)
