# Tech Book Generator

专业技术文档生成器，支持多主题配色

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 功能特点

- 📚 专业技术教程风格排版
- 🎨 **多主题配色**：科技蓝、经典橙、翡翠绿、紫罗兰、玫瑰红、深海蓝
- 📝 中英文双语标题支持
- 📊 自动生成目录 (TOC)
- 📄 HTML → PDF 转换
- 📖 支持对比表格、代码块、强调框
- 🖨️ **打印优化**：黄金比例边距、避免跨页分割、深色代码块自动变浅

## 默认主题

**科技蓝** (`#3498db`) - 专业、清爽、技术感强

## 快速开始

### 安装依赖

```bash
# 安装 Python 依赖（可选，用于 PDF 转换）
pip3 install playwright
playwright install chromium
```

### 基本用法

```bash
# 生成 HTML（使用默认科技蓝主题）
python3 generator.py \
  --title "我的教程" \
  --author "作者名" \
  --input content.md \
  --output output.html

# 生成 HTML 和 PDF
python3 generator.py \
  --title "我的教程" \
  --author "作者名" \
  --input content.md \
  --pdf

# 使用不同主题
python3 generator.py \
  --title "我的教程" \
  --author "作者名" \
  --input content.md \
  --theme green   # 可选: blue, orange, green, purple, red, dark
```

### 完整示例

```bash
python3 generator.py \
  --title "React 进阶指南" \
  --author "张三" \
  --subtitle "从入门到精通" \
  --theme blue \
  --keywords "React · 前端 · JavaScript" \
  --audience "前端开发者" \
  --input content.md \
  --output react-guide.html \
  --pdf
```

## 命令行参数

| 参数 | 说明 | 必需 |
|------|------|------|
| `--title` | 书籍标题 | ✅ |
| `--author` | 作者名称 | ✅ |
| `--input` / `-i` | 输入 Markdown 文件 | ✅ |
| `--output` / `-o` | 输出 HTML 文件 | ❌ |
| `--subtitle` | 副标题 | ❌ |
| `--series` | 系列名称 (默认: 技术文档) | ❌ |
| `--version` | 版本号 | ❌ |
| `--keywords` | 关键词 (用 · 分隔) | ❌ |
| `--audience` | 目标读者 | ❌ |
| `--theme` | 主题配色 (默认: blue) | ❌ |
| `--pdf` | 同时生成 PDF | ❌ |
| `--template` / `-t` | 自定义 HTML 模板 | ❌ |

## 主题配色

| 主题 | 颜色 | 风格 | 推荐场景 |
|------|------|------|----------|
| `blue` | 科技蓝 | 专业清爽 | 编程、AI、云技术（默认） |
| `orange` | 经典橙 | 温暖活力 | 教程、入门指南 |
| `green` | 翡翠绿 | 清新护眼 | 长篇文档、实践指南 |
| `purple` | 紫罗兰 | 现代独特 | 创新技术 |
| `red` | 玫瑰红 | 热情现代 | 前端开发 |
| `dark` | 深海蓝 | 稳重权威 | 企业文档、架构设计 |

## Markdown 格式

你的 Markdown 文件应该遵循以下格式：

```markdown
---
title: 主标题
subtitle: 副标题
series: 技术文档
author: 作者名
version: v260409
keywords: 关键词1 · 关键词2 · 关键词3
audience: 目标读者
---

# Part 1: 概念

## §01 章节标题
Section Subtitle

章节内容...

### 子标题

更多内容...

> **核心建议**
>
> 重点强调的内容

| 特性 | 说明 |
|------|------|
| 功能1 | 描述1 |

```code
代码示例
```
```

## 设计规范

### 章节标题格式
```
## §01 章节标题
Section Subtitle in English
```

### 强调框
```markdown
> **核心建议**
>
> 你的建议内容...
```

### 对比表格
```markdown
| 维度 | 工具A | 工具B |
|------|-------|-------|
| 特性1 | 说明A | 说明B |
```

## PDF 转换

### 方法 1: Playwright（推荐）

```bash
pip3 install playwright
playwright install chromium
```

使用 `--pdf` 参数自动转换。

### 方法 2: 浏览器打印

```bash
# 在浏览器中打开 HTML
open output.html

# 按 Cmd+P (Mac) 或 Ctrl+P (Windows/Linux)
# 选择"另存为 PDF"
```

## 示例

查看 `example-enhanced.md` 获取完整示例内容。

```bash
python3 generator.py \
  --title "Tech Book Generator 演示" \
  --author "Your Name" \
  --input example-enhanced.md \
  --output demo.html \
  --pdf
```

## 项目结构

```
tech-book-generator/
├── generator.py           # 主程序
├── template.html          # HTML 模板
├── example.md             # 基础示例
├── example-enhanced.md    # 完整示例
├── html2pdf.sh            # 浏览器打印脚本
├── README.md              # 本文档
└── LICENSE                # MIT 许可证
```

## 版本历史

### v2.0.0 (2026-04-09)
- ✨ 新增多主题配色系统（6 种主题）
- 🎨 默认主题改为科技蓝
- 🖨️ 打印优化（黄金比例边距、避免跨页分割）
- 💬 中西文混排间距修正
- 🎨 代码块颜色优化（VS Code Dark 风格）
- 🌈 章节分隔页渐变效果

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

- 设计灵感来源于 O'Reilly Media 和 The Pragmatic Programmer
- 参考了 W3C 中文排版标准 (CLREQ)
- 使用 Van de Graaf canon 进行页面布局
