---
title: Orange Book Generator
subtitle: 从入门到精通
series: 橙皮书
author: Claude
version: v260409
keywords: PDF生成 · HTML模板 · 技术文档 · 中文排版
audience: 需要创建专业技术教程的开发者
---

# Part 1: 概念

## §01 什么是橙皮书风格

Orange Book Style Guide

橙皮书风格是一种专为中文技术教程设计的排版风格，具有以下特点：

**视觉设计：**
- 橙色主题（橙皮书 branding）
- 专业的字体排版
- 中英文双语标题
- 清晰的层级结构

**内容结构：**
- 封面页：系列名称、标题、副标题、版本信息
- 目录页：按 Part 和 § 编号组织的章节
- 正文页：带编号的章节、子标题、内容

### 设计原则

这种风格注重可读性和专业性，适合技术教程、框架指南、API文档等内容。

## §02 核心设计元素

Core Design Elements

| 元素 | 说明 | 用途 |
|------|------|------|
| 封面页 | 展示书籍基本信息 | 第一印象 |
| 目录页 | 结构化内容导航 | 快速定位 |
| 章节标题 | §编号 + 中英文 | 清晰层级 |
| 对比表格 | 工具/框架对比 | 信息展示 |
| 核心建议 | 重点强调框 | 关键要点 |

> **核心建议**
>
> 使用橙皮书风格时，保持一致性非常重要。所有章节都应该遵循相同的编号规则和格式。

# Part 2: 动手实践

## §03 快速开始

Quick Start

使用 Orange Book Generator 生成文档：

```bash
# 生成 HTML
python generator.py \
  --title "我的教程" \
  --author "作者名" \
  --input content.md \
  --output output.html

# 生成 PDF
python generator.py \
  --title "我的教程" \
  --author "作者名" \
  --input content.md \
  --pdf
```

### 内容格式

使用 Markdown 编写内容，支持：

1. **Part 分组**：`# Part 1: 概念`
2. **章节编号**：`## §01 章节标题`
3. **英文副标题**：章节下一行
4. **表格**：标准 Markdown 表格
5. **强调框**：引用块格式

## §04 实战案例

Real World Example

让我们创建一个完整的文档示例：

**步骤一**：准备 Markdown 内容
**步骤二**：运行生成器
**步骤三**：查看 HTML 在浏览器中的效果
**步骤四**：转换为 PDF（可选）

> **核心建议**
>
> 在转换为 PDF 之前，务必在浏览器中预览 HTML 效果。这样可以提前发现排版问题。
