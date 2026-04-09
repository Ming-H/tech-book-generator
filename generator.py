#!/usr/bin/env python3
"""
Tech Book Generator - Generate professional technical tutorials in HTML/PDF format
Supports multiple color themes and print-optimized layout.

Usage:
    python generator.py --title "标题" --author "作者" --input content.md --output output.html
    python generator.py --title "标题" --author "作者" --input content.md --pdf
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime
import subprocess


class TechBookGenerator:
    """Generate Orange Book style HTML/PDF from markdown content."""

    # Language display name mapping
    LANG_DISPLAY = {
        'python': 'Python', 'py': 'Python',
        'javascript': 'JavaScript', 'js': 'JavaScript',
        'typescript': 'TypeScript', 'ts': 'TypeScript',
        'bash': 'Bash', 'shell': 'Bash', 'sh': 'Bash',
        'css': 'CSS',
        'html': 'HTML',
        'json': 'JSON',
        'sql': 'SQL',
        'yaml': 'YAML', 'yml': 'YAML',
        'xml': 'XML',
        'markdown': 'Markdown', 'md': 'Markdown',
        'dockerfile': 'Dockerfile',
        'makefile': 'Makefile',
    }

    # Theme color palettes
    THEMES = {
        'blue': {
            'primary': '#3498db',
            'primary-dark': '#2980b9',
            'accent-teal': '#1abc9c',
            'accent-blue': '#3498db',
            'accent-amber': '#f39c12',
            'accent-pink': '#e91e63',
            'callout-border': '#3498db',
            'primary-bg-light': 'rgba(52, 152, 219, 0.05)',
        },
        'orange': {
            'primary': '#e67e22',
            'primary-dark': '#d35400',
            'accent-teal': '#16a085',
            'accent-blue': '#2980b9',
            'accent-amber': '#f39c12',
            'accent-pink': '#e91e63',
            'callout-border': '#e67e22',
            'primary-bg-light': 'rgba(230, 126, 34, 0.05)',
        },
        'green': {
            'primary': '#27ae60',
            'primary-dark': '#229954',
            'accent-teal': '#16a085',
            'accent-blue': '#3498db',
            'accent-amber': '#f39c12',
            'accent-pink': '#e91e63',
            'callout-border': '#27ae60',
            'primary-bg-light': 'rgba(39, 174, 96, 0.05)',
        },
        'purple': {
            'primary': '#9b59b6',
            'primary-dark': '#8e44ad',
            'accent-teal': '#1abc9c',
            'accent-blue': '#3498db',
            'accent-amber': '#f39c12',
            'accent-pink': '#e91e63',
            'callout-border': '#9b59b6',
            'primary-bg-light': 'rgba(155, 89, 182, 0.05)',
        },
        'red': {
            'primary': '#e74c3c',
            'primary-dark': '#c0392b',
            'accent-teal': '#1abc9c',
            'accent-blue': '#3498db',
            'accent-amber': '#f39c12',
            'accent-pink': '#e91e63',
            'callout-border': '#e74c3c',
            'primary-bg-light': 'rgba(231, 76, 60, 0.05)',
        },
        'dark': {
            'primary': '#2c3e50',
            'primary-dark': '#1a252f',
            'accent-teal': '#1abc9c',
            'accent-blue': '#3498db',
            'accent-amber': '#f39c12',
            'accent-pink': '#e91e63',
            'callout-border': '#2c3e50',
            'primary-bg-light': 'rgba(44, 62, 80, 0.05)',
        },
    }

    def __init__(self, title, author, version=None, subtitle=None, series="技术文档",
                 keywords=None, audience=None, theme='blue'):
        self.title = title
        self.author = author
        self.version = version or f"v{datetime.now().strftime('%y%m%d')}"
        self.subtitle = subtitle or ""
        self.series = series
        self.keywords = keywords or ""
        self.audience = audience or ""
        self.theme = theme
        self.sections = []
        self.parts = []

    def parse_markdown(self, content):
        """Parse markdown content and extract structure."""
        lines = content.split('\n')
        current_part = None
        current_section = None
        current_content = []

        for line in lines:
            # Extract frontmatter
            if line.startswith('---'):
                continue
            if ':' in line and not current_part:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                if key == 'title':
                    self.title = value
                elif key == 'subtitle':
                    self.subtitle = value
                elif key == 'series':
                    self.series = value
                elif key == 'author':
                    self.author = value
                elif key == 'version':
                    self.version = value
                elif key == 'keywords':
                    self.keywords = value
                elif key == 'audience':
                    self.audience = value
                continue

            # Part headers (# Part 1: 概念)
            part_match = re.match(r'^#\s+Part\s+\d+:\s*(.+)', line)
            if part_match:
                if current_part:
                    self.parts.append(current_part)
                current_part = {
                    'title': part_match.group(1),
                    'sections': []
                }
                continue

            # Section headers (## §01 标题)
            section_match = re.match(r'^##\s+§(\d+)\s+(.+)', line)
            if section_match:
                if current_section and current_part:
                    current_part['sections'].append(current_section)
                # Initialize current_part if it doesn't exist
                if not current_part:
                    current_part = {
                        'title': '正文',
                        'sections': []
                    }
                current_section = {
                    'number': section_match.group(1),
                    'title': section_match.group(2),
                    'subtitle': '',
                    'content': ''
                }
                continue

            # English subtitle (next line after section)
            if current_section and not current_section['subtitle']:
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and not any(c in stripped for c in '。！？'):
                    # Check if it looks like English (contains Latin letters)
                    if re.search(r'[a-zA-Z]', stripped) and len(stripped) < 100:
                        current_section['subtitle'] = stripped
                        continue

            # Content
            if current_section:
                current_section['content'] += line + '\n'

        # Don't forget the last section and part
        if current_section and current_part:
            current_part['sections'].append(current_section)
        if current_part:
            self.parts.append(current_part)

    def render_content(self, content):
        """Convert markdown content to HTML."""
        html = content

        # Headers
        html = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

        # Bold
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

        # Italic
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

        # Inline code
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)

        # Code blocks with syntax highlighting and language label
        def highlight_code(match):
            lang = match.group(1) or ''
            code = match.group(2)
            code = self._apply_syntax_highlighting(code, lang)
            lang_class = lang if lang else 'text'
            display = self.LANG_DISPLAY.get(lang, lang.upper() if lang else 'TEXT')
            header = f'<div class="code-block-header"><span class="code-block-lang">{display}</span></div>\n'
            return f'<div class="code-block">\n{header}<pre><code class="language-{lang_class}">{code}</code></pre>\n</div>'
        html = re.sub(r'```(\w+)?\n(.+?)```', highlight_code, html, flags=re.DOTALL)

        # Blockquotes and callout boxes
        html = self._process_blockquotes(html)

        # Flowcharts: → A → B → C
        html = re.sub(r'→\s*([^\n→]+)', r'<span class="flowchart-arrow">→</span> <span class="flowchart-box">\1</span>', html)

        # File tree patterns
        html = self._convert_file_trees(html)

        # Tables
        table_pattern = r'(\|.+?\|\n)+'
        def replace_table(match):
            lines = match.group(0).strip().split('\n')
            if len(lines) < 2:
                return match.group(0)

            rows = []
            for line in lines:
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                rows.append(cells)

            if not rows:
                return match.group(0)

            html_table = '<table>\n<thead><tr>'
            for cell in rows[0]:
                html_table += f'<th>{cell}</th>'
            html_table += '</tr></thead>\n<tbody>'

            for row in rows[2:] if len(rows) > 2 else rows[1:]:
                html_table += '<tr>'
                for cell in row:
                    html_table += f'<td>{cell}</td>'
                html_table += '</tr>\n'

            html_table += '</tbody></table>\n'
            return html_table

        html = re.sub(table_pattern, replace_table, html)

        # Links
        html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)

        # Horizontal rule
        html = re.sub(r'^---$', '<hr>', html, flags=re.MULTILINE)

        # Lists (unordered, ordered, and process steps)
        html = self._process_lists(html)

        # Paragraphs (but avoid HTML tags)
        html = re.sub(r'^(?!<[hbp]|<ul|<ol|<tab|<bl|<hr|<d|<f|<div|<li)(.+)$', r'<p>\1</p>', html, flags=re.MULTILINE)

        return html

    # --- HTML Escaping ---

    def _escape_html(self, code):
        """Escape HTML special characters in code."""
        return code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # --- Syntax Highlighting ---

    def _apply_syntax_highlighting(self, code, lang):
        """Apply syntax highlighting based on language."""
        lang = (lang or '').lower()
        dispatchers = {
            'python': self._highlight_python, 'py': self._highlight_python,
            'bash': self._highlight_bash, 'shell': self._highlight_bash, 'sh': self._highlight_bash,
            'javascript': self._highlight_javascript, 'js': self._highlight_javascript,
            'typescript': self._highlight_javascript, 'ts': self._highlight_javascript,
            'css': self._highlight_css,
            'html': self._highlight_html,
        }
        highlighter = dispatchers.get(lang, self._highlight_generic)
        return highlighter(code)

    def _highlight_python(self, code):
        """Python syntax highlighting."""
        code = self._escape_html(code)
        code = re.sub(r'(#.*)$', r'<span class="syntax-comment">\1</span>', code, flags=re.MULTILINE)
        code = re.sub(r'"""(.+?)"""', r'<span class="syntax-string">"""\1"""</span>', code, flags=re.DOTALL)
        code = re.sub(r"'''(.+?)'''", r"<span class=\"syntax-string\">'''\1'''</span>", code, flags=re.DOTALL)
        code = re.sub(r'"([^"]*)"', r'<span class="syntax-string">"\1"</span>', code)
        code = re.sub(r"'([^']*)'", r"<span class=\"syntax-string\">'\1'</span>", code)
        code = re.sub(r'\b(def)\s+(\w+)', r'<span class="syntax-keyword">\1</span> <span class="syntax-function">\2</span>', code)
        code = re.sub(r'\b(class)\s+(\w+)', r'<span class="syntax-keyword">\1</span> <span class="syntax-class">\2</span>', code)
        code = re.sub(r'@(\w+)', r'<span class="syntax-function">@\1</span>', code)
        keywords = ['import', 'from', 'return', 'if', 'else', 'elif', 'for', 'while',
                     'try', 'except', 'with', 'as', 'True', 'False', 'None', 'pass',
                     'break', 'continue', 'raise', 'finally', 'yield', 'lambda', 'and', 'or', 'not', 'in', 'is']
        for kw in keywords:
            code = re.sub(rf'\b{kw}\b', f'<span class="syntax-keyword">{kw}</span>', code)
        code = re.sub(r'\b(\d+\.?\d*)\b', r'<span class="syntax-number">\1</span>', code)
        return code

    def _highlight_bash(self, code):
        """Bash/Shell syntax highlighting."""
        code = self._escape_html(code)
        code = re.sub(r'(#.*)$', r'<span class="syntax-comment">\1</span>', code, flags=re.MULTILINE)
        code = re.sub(r'"([^"]*)"', r'<span class="syntax-string">"\1"</span>', code)
        code = re.sub(r"'([^']*)'", r"<span class=\"syntax-string\">'\1'</span>", code)
        code = re.sub(r'\$(\w+)', r'<span class="syntax-variable">$\1</span>', code)
        code = re.sub(r'\$\{([^}]+)\}', r'<span class="syntax-variable">${\1}</span>', code)
        code = re.sub(r'(\s)(-{1,2}[\w-]+)', r'\1<span class="syntax-property">\2</span>', code)
        keywords = ['if', 'then', 'else', 'elif', 'fi', 'for', 'while', 'do', 'done',
                     'case', 'esac', 'function', 'return', 'export', 'source', 'alias',
                     'echo', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'cat', 'grep', 'sed', 'awk',
                     'find', 'chmod', 'chown', 'sudo', 'apt', 'yum', 'brew', 'pip', 'npm',
                     'git', 'docker', 'curl', 'wget', 'vim', 'nano', 'ls', 'pwd', 'touch',
                     'tail', 'head', 'sort', 'uniq', 'wc', 'xargs', 'tee', 'ln', 'tar',
                     'ssh', 'scp', 'rsync', 'kill', 'ps', 'top', 'env', 'which', 'man']
        for kw in keywords:
            code = re.sub(rf'\b{kw}\b', f'<span class="syntax-keyword">{kw}</span>', code)
        code = re.sub(r'\b(\d+)\b', r'<span class="syntax-number">\1</span>', code)
        return code

    def _highlight_javascript(self, code):
        """JavaScript/TypeScript syntax highlighting."""
        code = self._escape_html(code)
        code = re.sub(r'(//.*)$', r'<span class="syntax-comment">\1</span>', code, flags=re.MULTILINE)
        code = re.sub(r'/\*(.+?)\*/', r'<span class="syntax-comment">/*\1*/</span>', code, flags=re.DOTALL)
        code = re.sub(r'"([^"]*)"', r'<span class="syntax-string">"\1"</span>', code)
        code = re.sub(r"'([^']*)'", r"<span class=\"syntax-string\">'\1'</span>", code)
        code = re.sub(r'`([^`]*)`', r'<span class="syntax-string">`\1`</span>', code)
        code = re.sub(r'\b(function)\s+(\w+)', r'<span class="syntax-keyword">\1</span> <span class="syntax-function">\2</span>', code)
        code = re.sub(r'\b(class)\s+(\w+)', r'<span class="syntax-keyword">\1</span> <span class="syntax-class">\2</span>', code)
        code = re.sub(r'\b(\w+)\s*\(', r'<span class="syntax-function">\1</span>(', code)
        code = re.sub(r'=>', '<span class="syntax-operator">=&gt;</span>', code)
        keywords = ['const', 'let', 'var', 'return', 'if', 'else', 'for', 'while',
                     'new', 'this', 'async', 'await', 'import', 'export', 'from',
                     'default', 'try', 'catch', 'throw', 'typeof', 'instanceof',
                     'true', 'false', 'null', 'undefined', 'switch', 'case', 'break',
                     'continue', 'extends', 'super', 'static', 'yield', 'of', 'in']
        for kw in keywords:
            code = re.sub(rf'\b{kw}\b', f'<span class="syntax-keyword">{kw}</span>', code)
        code = re.sub(r'\b(\d+\.?\d*)\b', r'<span class="syntax-number">\1</span>', code)
        return code

    def _highlight_css(self, code):
        """CSS syntax highlighting."""
        code = self._escape_html(code)
        code = re.sub(r'/\*(.+?)\*/', r'<span class="syntax-comment">/*\1*/</span>', code, flags=re.DOTALL)
        code = re.sub(r'"([^"]*)"', r'<span class="syntax-string">"\1"</span>', code)
        code = re.sub(r"'([^']*)'", r"<span class=\"syntax-string\">'\1'</span>", code)
        at_rules = ['@media', '@keyframes', '@import', '@font-face', '@charset', '@supports']
        for rule in at_rules:
            code = re.sub(rf'\b{re.escape(rule)}\b', f'<span class="syntax-keyword">{rule}</span>', code)
        properties = ['color', 'background', 'border', 'margin', 'padding', 'font', 'display',
                      'position', 'width', 'height', 'flex', 'grid', 'transition', 'animation',
                      'transform', 'opacity', 'overflow', 'box-shadow', 'text-align', 'line-height',
                      'letter-spacing', 'font-size', 'font-weight', 'font-family', 'max-width',
                      'min-width', 'z-index', 'top', 'right', 'bottom', 'left', 'content',
                      'cursor', 'visibility', 'white-space', 'word-break', 'border-radius',
                      'justify-content', 'align-items', 'gap', 'padding', 'margin']
        for prop in properties:
            code = re.sub(rf'\b{prop}\s*:', f'<span class="syntax-property">{prop}</span>:', code)
        code = re.sub(r'(\.[\w-]+)', r'<span class="syntax-class">\1</span>', code)
        code = re.sub(r'(#[\w-]+)', r'<span class="syntax-variable">\1</span>', code)
        code = re.sub(r'(::?[\w-]+)', r'<span class="syntax-function">\1</span>', code)
        code = re.sub(r'\b(\d+\.?\d*)(px|em|rem|%|vh|vw|s|ms|deg)?\b', r'<span class="syntax-number">\1\2</span>', code)
        code = re.sub(r'(#[0-9a-fA-F]{3,8})\b', r'<span class="syntax-number">\1</span>', code)
        return code

    def _highlight_html(self, code):
        """HTML syntax highlighting."""
        code = self._escape_html(code)
        code = re.sub(r'(&lt;!--.+?--&gt;)', r'<span class="syntax-comment">\1</span>', code, flags=re.DOTALL)
        code = re.sub(r'"([^"]*)"', r'<span class="syntax-string">"\1"</span>', code)
        code = re.sub(r"'([^']*)'", r"<span class=\"syntax-string\">'\1'</span>", code)
        code = re.sub(r'(&lt;/?)([\w-]+)', r'\1<span class="syntax-keyword">\2</span>', code)
        code = re.sub(r'\s([\w-]+)=', r' <span class="syntax-property">\1</span>=', code)
        code = re.sub(r'\b(\d+)\b', r'<span class="syntax-number">\1</span>', code)
        return code

    def _highlight_generic(self, code):
        """Generic syntax highlighting for unknown languages."""
        code = self._escape_html(code)
        code = re.sub(r'(#.*)$', r'<span class="syntax-comment">\1</span>', code, flags=re.MULTILINE)
        code = re.sub(r'"([^"]*)"', r'<span class="syntax-string">"\1"</span>', code)
        code = re.sub(r"'([^']*)'", r"<span class=\"syntax-string\">'\1'</span>", code)
        code = re.sub(r'\b(\d+\.?\d*)\b', r'<span class="syntax-number">\1</span>', code)
        return code

    # --- Blockquotes and Callout Boxes ---

    def _process_blockquotes(self, html):
        """Process blockquotes and callout boxes ([!NOTE], [!TIP], [!WARNING], [!DANGER], [!SUCCESS])."""
        CALLOUT_MAP = {
            'NOTE': ('info-box', '笔记'),
            'INFO': ('info-box', '信息'),
            'TIP': ('tip-box', '技巧'),
            'WARNING': ('warning-box', '警告'),
            'DANGER': ('danger-box', '危险'),
            'SUCCESS': ('success-box', '成功'),
        }

        lines = html.split('\n')
        result = []
        i = 0

        while i < len(lines):
            if re.match(r'^>\s', lines[i]):
                # Collect consecutive blockquote lines
                bq_lines = []
                while i < len(lines) and (re.match(r'^>\s', lines[i]) or lines[i].strip() == ''):
                    if re.match(r'^>\s', lines[i]):
                        bq_lines.append(lines[i])
                    elif bq_lines:
                        # Empty line inside blockquote — include as spacer
                        bq_lines.append('>')
                    i += 1

                # Strip '> ' prefix
                content_lines = []
                for line in bq_lines:
                    stripped = re.sub(r'^>\s?', '', line)
                    content_lines.append(stripped)
                content = '\n'.join(content_lines).strip()

                if not content:
                    continue

                # Check for callout type: first line matches [!TYPE]
                callout_match = re.match(r'^\[!(\w+)\]\s*$', content.split('\n')[0])
                if callout_match:
                    callout_type = callout_match.group(1).upper()
                    if callout_type in CALLOUT_MAP:
                        css_class, label = CALLOUT_MAP[callout_type]
                        # Remove the [!TYPE] line
                        body = '\n'.join(content.split('\n')[1:]).strip()
                        # Render bold labels in the body
                        body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', body)
                        result.append(f'<div class="{css_class}">\n<strong>{label}：</strong>{body}\n</div>')
                        continue

                # Standard blockquote
                content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
                content = re.sub(r'\n\n', '\n<br>\n', content)
                result.append(f'<blockquote>\n{content}\n</blockquote>')
            else:
                result.append(lines[i])
                i += 1

        return '\n'.join(result)

    # --- Lists ---

    def _process_lists(self, html):
        """Process unordered lists, ordered lists, and process steps."""
        lines = html.split('\n')
        result = []
        i = 0

        while i < len(lines):
            ul_match = re.match(r'^([-*])\s+(.+)$', lines[i])
            ol_match = re.match(r'^(\d+)\.\s+(.+)$', lines[i])

            if ul_match:
                # Collect consecutive unordered list items
                items = []
                while i < len(lines):
                    m = re.match(r'^[-*]\s+(.+)$', lines[i])
                    if m:
                        items.append(m.group(1))
                        i += 1
                    else:
                        break
                items_html = '\n'.join(f'<li>{item}</li>' for item in items)
                result.append(f'<ul>\n{items_html}\n</ul>')

            elif ol_match:
                # Collect consecutive ordered list items
                items = []
                while i < len(lines):
                    m = re.match(r'^\d+\.\s+(.+)$', lines[i])
                    if m:
                        items.append(m.group(1))
                        i += 1
                    else:
                        break

                if len(items) >= 2:
                    items_html = '\n'.join(f'<li>{item}</li>' for item in items)
                    result.append(f'<ol>\n{items_html}\n</ol>')
                else:
                    # Single item — use process-step with wrapper
                    items_html = '\n'.join(
                        f'<div class="process-step">{item}</div>' for item in items
                    )
                    result.append(f'<div class="process-steps">\n{items_html}\n</div>')

            else:
                result.append(lines[i])
                i += 1

        return '\n'.join(result)

    def _convert_file_trees(self, html):
        """Convert file tree patterns to styled HTML."""
        # Pattern: Lines starting with ├── or │ that form a tree structure
        lines = html.split('\n')
        result = []
        in_tree = False
        tree_lines = []

        for line in lines:
            # Check if this looks like a file tree
            if re.match(r'^[├│└]', line.strip()) or (in_tree and re.match(r'^\s*(│|├|└)', line)):
                in_tree = True
                tree_lines.append(line)
                # Check if tree continues
                if not re.match(r'^\s*(│|├|└)', line):
                    # Might be end of tree
                    if tree_lines:
                        result.append(self._format_file_tree(tree_lines))
                        tree_lines = []
                        in_tree = False
                    result.append(line)
            elif in_tree and not tree_lines:
                # Tree ended
                if tree_lines:
                    result.append(self._format_file_tree(tree_lines))
                result.append(line)
                tree_lines = []
                in_tree = False
            else:
                result.append(line)

        # Handle remaining tree
        if tree_lines:
            result.append(self._format_file_tree(tree_lines))

        return '\n'.join(result)

    def _format_file_tree(self, lines):
        """Format file tree lines as HTML."""
        html_lines = ['<div class="file-tree">']
        for line in lines:
            # Identify directories (ending with / or ─ coming from previous line)
            if '/' in line or '┬' in line:
                html_lines.append(f'<div class="file-tree-line file-tree-dir">{line}</div>')
            else:
                html_lines.append(f'<div class="file-tree-line file-tree-file">{line}</div>')
        html_lines.append('</div>')
        return '\n'.join(html_lines)

    def generate_toc(self):
        """Generate table of contents HTML."""
        toc_html = ''

        for part in self.parts:
            toc_html += f'<div class="toc-part">\n'
            toc_html += f'<div class="toc-part-title">Part {self.parts.index(part) + 1}: {part["title"]}</div>\n'

            for section in part['sections']:
                toc_html += '<div class="toc-item">\n'
                toc_html += f'<div class="toc-item-number">§{section["number"]}</div>\n'
                toc_html += f'<div class="toc-item-title">{section["title"]}</div>\n'
                toc_html += '<div class="toc-item-page">' + str(len(self.sections) + 1) + '</div>\n'
                toc_html += '</div>\n'
                self.sections.append(section)

            toc_html += '</div>\n'

        return toc_html

    def generate_content_body(self):
        """Generate main content HTML."""
        content_html = ''

        for part in self.parts:
            # Part header
            part_num = self.parts.index(part) + 1
            content_html += f'<div class="part-header">\n'
            content_html += f'<div class="part-number">PART {part_num}</div>\n'
            content_html += f'<div class="part-title">{part["title"]}</div>\n'
            content_html += '</div>\n'

            for section in part['sections']:
                # Section header
                content_html += '<div class="section-header">\n'
                content_html += f'<div class="section-number">§{section["number"]}</div>\n'
                content_html += f'<h2 class="section-title">{section["title"]}</h2>\n'
                if section['subtitle']:
                    content_html += f'<div class="section-subtitle">{section["subtitle"]}</div>\n'
                content_html += '</div>\n'

                # Section content
                content_html += self.render_content(section['content'])

        return content_html

    def generate_html(self, template_path=None):
        """Generate final HTML from template."""
        if template_path is None:
            template_path = Path(__file__).parent / 'template.html'

        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # Generate TOC and content
        toc_html = self.generate_toc()
        content_html = self.generate_content_body()

        # Apply theme colors
        theme_colors = self.THEMES.get(self.theme, self.THEMES['blue'])

        # Replace placeholders
        html = template.replace('{series}', self.series)
        html = html.replace('{title}', self.title)
        html = html.replace('{subtitle}', self.subtitle)
        html = html.replace('{keywords}', self.keywords)
        html = html.replace('{audience}', self.audience)
        html = html.replace('{version}', self.version)
        html = html.replace('{author_info}', self.author)
        html = html.replace('{footer_note}', f'本手册基于 {self.title} 编写。AI 工具迭代迅速，部分内容可能随版本更新而变化，请以官方文档为准。')
        html = html.replace('{toc_content}', toc_html)
        html = html.replace('{content_body}', content_html)

        # Apply theme colors (replace in :root section)
        html = re.sub(r'--primary:\s*#[0-9a-fA-F]{6}', f'--primary: {theme_colors["primary"]}', html)
        html = re.sub(r'--primary-dark:\s*#[0-9a-fA-F]{6}', f'--primary-dark: {theme_colors["primary-dark"]}', html)
        html = re.sub(r'--accent-teal:\s*#[0-9a-fA-F]{6}', f'--accent-teal: {theme_colors["accent-teal"]}', html)
        html = re.sub(r'--accent-blue:\s*#[0-9a-fA-F]{6}', f'--accent-blue: {theme_colors["accent-blue"]}', html)
        html = re.sub(r'--accent-amber:\s*#[0-9a-fA-F]{6}', f'--accent-amber: {theme_colors["accent-amber"]}', html)
        html = re.sub(r'--accent-pink:\s*#[0-9a-fA-F]{6}', f'--accent-pink: {theme_colors["accent-pink"]}', html)
        html = re.sub(r'--callout-border:\s*#[0-9a-fA-F]{6}', f'--callout-border: {theme_colors["callout-border"]}', html)
        html = re.sub(r'rgba\(52,\s*152,\s*219,\s*0\.05\)', theme_colors.get('primary-bg-light', 'rgba(52, 152, 219, 0.05)'), html)

        return html

    def convert_to_pdf(self, html_path, output_path=None):
        """Convert HTML to PDF using playwright (preferred) or browser fallback."""
        if output_path is None:
            output_path = html_path.replace('.html', '.pdf')

        # Try playwright first (best quality)
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f'file://{Path(html_path).absolute()}')
                page.wait_for_load_state('networkidle')
                page.pdf(
                    path=output_path,
                    format='A4',
                    margin={'top': '20mm', 'right': '20mm', 'bottom': '20mm', 'left': '20mm'},
                    print_background=True
                )
                browser.close()

            print(f"✓ PDF generated: {output_path}")
            return output_path

        except ImportError:
            # Fallback to browser-based conversion
            script_path = Path(__file__).parent / 'html2pdf.sh'
            if script_path.exists():
                result = subprocess.run(
                    ['bash', str(script_path), html_path, output_path],
                    capture_output=True,
                    text=True
                )
                print(result.stdout)
                return output_path
            else:
                print(f"Warning: Playwright not installed. Install with:")
                print(f"  pip3 install playwright")
                print(f"  playwright install chromium")
                print(f"\nOpening {html_path} in browser...")
                import webbrowser
                webbrowser.open(f'file://{Path(html_path).absolute()}')
                print("\nTo save as PDF:")
                print("1. Press Cmd+P (Mac) or Ctrl+P (Windows/Linux)")
                print("2. Choose 'Save as PDF' as destination")
                print("3. Click Save")
                return None
        except Exception as e:
            print(f"PDF conversion error: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(description='Generate Orange Book style HTML/PDF')
    parser.add_argument('--title', required=True, help='Book title')
    parser.add_argument('--author', required=True, help='Author name')
    parser.add_argument('--subtitle', help='Subtitle')
    parser.add_argument('--series', default='技术文档', help='Series name')
    parser.add_argument('--version', help='Version (default: auto-generated)')
    parser.add_argument('--keywords', help='Keywords separated by ·')
    parser.add_argument('--audience', help='Target audience')
    parser.add_argument('--input', '-i', required=True, help='Input markdown file')
    parser.add_argument('--output', '-o', help='Output HTML file')
    parser.add_argument('--pdf', action='store_true', help='Also generate PDF')
    parser.add_argument('--template', '-t', help='Custom HTML template')
    parser.add_argument('--theme', default='blue',
                        choices=['blue', 'orange', 'green', 'purple', 'red', 'dark'],
                        help='Color theme (default: blue)')

    args = parser.parse_args()

    # Read input
    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate HTML
    generator = TechBookGenerator(
        title=args.title,
        author=args.author,
        subtitle=args.subtitle,
        series=args.series,
        version=args.version,
        keywords=args.keywords,
        audience=args.audience,
        theme=args.theme
    )

    generator.parse_markdown(content)
    html = generator.generate_html(args.template)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input)
        output_path = input_path.stem + '.html'

    # Write HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Generated HTML: {output_path}")
    print(f"  Theme: {args.theme}")

    # Convert to PDF if requested
    if args.pdf:
        pdf_path = output_path.replace('.html', '.pdf')
        result = generator.convert_to_pdf(output_path, pdf_path)
        if result:
            print(f"✓ Generated PDF: {pdf_path}")
        else:
            print("✗ PDF conversion failed. Please install Playwright:")
            print("  pip3 install playwright && playwright install chromium")


if __name__ == '__main__':
    main()
