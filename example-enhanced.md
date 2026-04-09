---
title: Orange Book 增强版
subtitle: 完整样式演示
series: 橙皮书
author: Claude
version: v260409
keywords: 代码高亮 · 流程图 · 文件树 · 彩色框 · 样式演示
audience: 技术文档编写者
---

# Part 1: 样式演示

## §01 代码语法高亮
Syntax Highlighting Demo

现在支持代码语法高亮了！这是 Python 示例：

```python
def hermes_agent():
    """Hermes Agent 主函数"""
    # 初始化配置
    config = {
        "model": "claude-3",
        "temperature": 0.7,
        "max_tokens": 4096
    }
    
    # 执行任务
    result = agent.run(config)
    return result

# 调用函数
hermes_agent()
```

JavaScript 示例：

```javascript
function createAgent(name, type) {
    const agent = {
        name: name,
        type: type || 'default',
        skills: []
    };
    return agent;
}
```

> **核心建议**
>
> 新版本支持语法高亮了！代码块现在有深色背景和彩色语法高亮，包括：
> - 关键字（紫色）
> - 字符串（绿色）
> - 数字（橙色）
> - 注释（灰色斜体）

## §02 流程图和图表
Diagrams and Flowcharts

这是流程图示例：

输入 → 处理 → 存储 → 输出

学习循环示例：

用户输入 → 创建Skill → Skill改进 → 记忆存储 → 用户建模 → 更好的输出

## §03 文件树结构
File Tree Structure

支持文件系统树形结构：

~/.hermes/
├── bundled/           # 内置Skill
│   ├── research/
│   └── development/
├── skills/            # 用户创建的Skill
│   ├── github-daily.md
│   └── code-review.md
└── memory.db          # 记忆数据库

## §04 多种强调框
Colored Callout Boxes

### 信息框

<div class="info-box">
<strong>提示：</strong>这是信息提示框，用于一般性说明。
</div>

### 成功框

<div class="success-box">
<strong>成功：</strong>这是成功提示框，用于表示操作成功完成。
</div>

### 警告框

<div class="warning-box">
<strong>警告：</strong>这是警告提示框，用于提醒注意事项。
</div>

### 技巧框

<div class="tip-box">
<strong>技巧：</strong>这是技巧提示框，用于分享实用技巧。
</div>

## §05 步骤列表
Process Steps

按照以下步骤配置：

1. 安装依赖：`pip install playwright`
2. 初始化项目：`npm init`
3. 配置环境变量
4. 运行测试
5. 部署上线

## §06 高亮框
Highlight Box

<div class="highlight-box">
<strong>重要提示：</strong>

学习循环的效果和你的使用频率直接相关。如果你一周只用一两次，改进会很慢。但如果你把它当作日常工作伙伴，每天都会用，飞轮转得会非常快。
</div>

# Part 2: 实战应用

## §07 综合示例
Complete Example

结合所有样式的完整示例：

```bash
# Hermes Agent 安装
git clone https://github.com/nousresearch/hermes-agent.git
cd hermes-agent

# 配置环境
cp .env.example .env
vim .env

# 启动服务
python hermes &
```

> **核心建议**
>
> 安装完成后，确保配置正确的 LLM API 密钥。推荐使用 OpenRouter 或 Anthropic API。

文件结构：

hermes-agent/
├── skills/         # 技能目录
├── tools/          # 工具目录
├── agents/         # Agent 配置
└── cli.py          # 主入口

配置流程：

API配置 → 部署设置 → 平台接入 → 测试验证 → 正式使用

---

**现在橙皮书生成器支持：**

✅ **代码语法高亮** - Python、JavaScript 等多语言彩色高亮
✅ **深色代码背景** - 深蓝色背景 (#1e293b) 更护眼
✅ **流程图样式** - 带箭头的流程图展示
✅ **文件树结构** - 模拟文件系统的树形显示
✅ **多种强调框** - 信息、成功、警告、技巧四种样式
✅ **步骤列表** - 自动编号的步骤列表
✅ **高亮框** - 用于重点内容的强调

所有样式都已针对 PDF 导出优化！
