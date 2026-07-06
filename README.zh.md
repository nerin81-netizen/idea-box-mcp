# 🧠 idea-box-mcp

> **用自然语言搜索和添加本地 Markdown 知识库(idea-box + memo-box)。就这么简单。**

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/idea-box-mcp)](https://github.com/nerin81-netizen/idea-box-mcp/stargazers)

**🌍 选择语言:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

[🚀 快速开始](#-快速开始) · [🛠 工具](#-工具5个) · [🎬 演示](#-演示) · [🏗 架构](#-架构) · [🧪 开发](#-开发)

---

## ✨ 这是什么？

**你的文件夹里堆满了 Markdown 文件。** 收集的想法、备忘录、链接、参考资料。你知道它们就在那儿——但真要用的时候，找起来可太麻烦了。

`idea-box-mcp` 把你的本地 Markdown 文件夹变成了 **LLM 可以直接调用的工具**。不用再：

```bash
# ❌ 以前：手动搜索
grep -r "AI" ~/ideas-h/
find ~/memos-h/ -name "*.md" -exec grep -l "arxiv" {} \;
```

现在你可以直接说：

```text
# ✅ 现在：自然语言
"帮我找找 AI 相关的想法"
"给我看看 arxiv 的备忘录"
"记一下——这个链接以后要看"
```

**提供两个目录：**

| 目录 | 里面有什么 | 什么时候用 |
|---|---|---|
| `~/ideas-h/` | 应用想法（带状态/评级） | "接下来该做啥？" |
| `~/memos-h/` | 原始参考资料（8个分类） | "之前存了什么来着？" |

> **核心理念：** 你的本地 Markdown 文件夹本身就是知识库。这个 MCP 只是让 LLM 能 *搜索* 它们而已。

## 🛠 工具 (5个)

| 工具 | 参数 | 说明 | 示例提示 |
|---|---|---|---|
| `search_ideas` | `keyword`, `limit` | 按关键词搜索 idea-box | "帮我找 AI 相关的想法" |
| `count_ideas` | — | 统计（总数、评级分布、最近） | "我有多少想法？" |
| `search_memos` | `keyword`, `category`, `limit` | 搜索 memo-box（8个分类） | "找找 arxiv 的备忘录" |
| `count_memos` | — | 统计（总数、按分类） | "看看 memo-box 统计" |
| `add_memo` | `title`, `content`, `category`, `tags` | 添加新备忘录（自动分类） | "记一下——..." |

### 实际场景

**场景 1："那个健康追踪的想法放哪了？"**

记得两周前写过关于健康应用的东西，但找不到了。直接问：

```text
"帮我找找健康相关的想法"

→ 🔍 '健康' 搜索结果 — 3条 / 共145条

  · **健康数据整合 App** [B]
    把医院/药店/保险数据放一起...
    📁 `2026-06-15_健康数据整合 App.md`

  · **用药提醒+相互作用检查**
    吃药时检查副作用的应用...
    📁 `2026-06-20_用药提醒.md`
```

**场景 2："先存着，以后看"**

刷网页时发现有趣的东西。别加书签然后忘掉，直接说：

```text
"记一下——vLLM 部署教程: https://vllm.readthedocs.io/en/latest/
标签: mlops, inference, vllm"

→ ✅ 已保存: `links/2026-07-06_vLLM 部署教程.md`
   分类: 🔗 链接
```

之后可以问：

```text
"帮我找找 inference 相关的备忘录"

→ 🔍 备忘录搜索 — 2条 / 共11条

  · 🔗 链接 **vLLM 部署教程**
    https://vllm.readthedocs.io/en/latest/
    📁 `links/2026-07-06_vLLM 部署教程.md`
```

**场景 3："我有多少想法？"**

```text
"我有多少想法？"

→ 📊 想法箱状态

📁 共 145 条
🥇 S 级: 0条
🥈 A 级: 1条
🥉 B 级: 0条
⚪ C 级: 0条

**最近添加的 5 条:**
  · 🧠 [最近添加的想法标题 1]
  · 📋 [最近添加的想法标题 2]
  · 📰 [最近添加的想法标题 3]
  · …
```

### `search_ideas(keyword, limit=5)`

在 idea-box 文件中按关键词搜索标题+内容。返回标题、摘要、评级(S/A/B/C)、文件路径。

### `count_ideas()`

返回总数、评级分布(S/A/B/C)、最近 5 条想法。

### `search_memos(keyword="", category="", limit=10)`

搜索 memo-box。可选的 `category` 过滤：
`links` · `news` · `quotes` · `references` · `snippets` · `specs` · `tips` · `misc`

### `count_memos()`

返回总数、按分类的统计、最近 3 条备忘录。

### `add_memo(title, content, category="", tags="")`

添加新备忘录。`category` 留空则服务端自动分类：
- 含 URL → `links`
- 代码/命令/配置 → `snippets`
- 引用/引号内容 → `quotes`
- 新闻关键词 → `news`
- 规格/需求 → `specs`
- 教程/错误修复 → `tips`
- 论文/书籍/链接 → `references`
- 默认 → `misc`

返回文件路径和检测到的分类。

## 🚀 快速开始

### 安装

```bash
pip install idea-box-mcp
```

或从源码安装：

```bash
git clone https://github.com/nerin81-netizen/idea-box-mcp
cd idea-box-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### 配置路径

默认情况下，服务器读取：
- Idea-box: `~/ideas-h/`
- Memo-box: `~/memos-h/`

如需更改，编辑 `server.py` 顶部常量：

```python
IDEA_DIR = Path("/你的/路径/ideas-h")
MEMO_DIR = Path("/你的/路径/memos-h")
```

### 注册到 MCP 客户端

#### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "idea-box": {
      "command": "idea-box-mcp"
    }
  }
}
```

#### Cursor / Cline

`.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "idea-box": {
      "command": "idea-box-mcp"
    }
  }
}
```

## 🎬 演示

### 搜索想法

```text
👤 帮我找找 AI 相关的想法

🤖 Claude:
🔍 'AI' 搜索结果 — 139条 / 共145条

  · **心灵成长日记**
    每天写简单日记，感受心灵成长的 App …
    📁 `2026-06-28_心灵成长日记.md`

  · **口袋黑匣子**
    手机在口袋里自动录下一天的对话 …
    📁 `2026-06-28_口袋黑匣子.md`
```

### 想法箱统计

```text
👤 我有多少想法？

🤖 Claude:
📊 **想法箱状态**

📁 共 145 条
🥇 S 级: 0条
🥈 A 级: 1条
🥉 B 级: 0条
⚪ C 级: 0条

**最近添加的 5 条:**
  · 🧠 [最近添加的想法标题 1]
  · 📋 [最近添加的想法标题 2]
  · 📰 [最近添加的想法标题 3]
  · …
```

（实际标题取决于你本地 `~/ideas-h/` 目录的内容。）

### 搜索备忘录

```text
👤 看看 memo-box 统计

🤖 Claude:
📊 **备忘录状态** — 共 11 条

  💬 引用/句子: 7条
  🔗 链接: 2条
  📦 其他: 1条
  🛠️ 技巧/方案: 1条
```

### 添加备忘录

```text
👤 记一下——GitHub PAT 安全推送模式
       export GH_TOKEN=YOUR_TOKEN && git push 后清理 git remote set-url。
       https://github.com/settings/tokens 撤销。
       标签: github, security, mcp-publish

🤖 Claude:
✅ 已保存: `links/2026-07-06_GitHub PAT 安全推送模式.md`
   分类: 🔗 链接
```

## 🏗 架构

```
┌─────────────────┐      stdio/JSON-RPC      ┌──────────────────────┐
│  LLM Client     │ ◀──────────────────────▶ │  idea-box-mcp        │
│  (Claude/Cursor) │                          │  (FastMCP server)    │
└─────────────────┘                          └──────────┬───────────┘
                                                        │ pathlib
                                            ┌───────────┴────────────┐
                                            ▼                        ▼
                                    ┌──────────────┐         ┌──────────────┐
                                    │  ~/ideas-h/  │         │  ~/memos-h/  │
                                    │  *.md files  │         │  8 subdirs   │
                                    └──────────────┘         └──────────────┘
```

**关键设计决策：**

- **stdio transport** — MCP 标准
- **FastMCP** — Anthropic 官方 Python SDK
- **零外部依赖**（除了 MCP）— 纯文件 I/O
- **idea-box 只读**（保护你的结构）+ **memo-box 可写**（添加新文件）
- **自动分类** — 简单的启发式规则（URL/代码/关键词）

## 🧪 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 直接测试 stdio JSON-RPC
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | idea-box-mcp

# 分类逻辑单元测试
python -c "
from idea_box_mcp.server import _detect_memo_category
print(_detect_memo_category('GitHub PAT', 'export GH_TOKEN=...'))
# → 'links'
print(_detect_memo_category('Bash script', 'pip install mcp'))
# → 'snippets'
"
```

## 🌍 路线图

- [x] v0.1.0 — 5个工具，stdio，idea-box + memo-box
- [ ] v0.2.0 — `add_idea` 工具（带状态/评级提示）
- [ ] v0.3.0 — 备忘录 `tag` 过滤 + 交叉搜索
- [ ] v0.4.0 — 想法状态转换 (💭 → 🔍 → 💼)
- [ ] v0.5.0 — 通过环境变量配置目录

## 🤝 贡献

欢迎提 Issue 和 PR。特别有用的：

- 📂 新的备忘录分类
- 🔍 更好的搜索（模糊匹配、语义搜索）
- 📝 idea-box 写入工具（小心——保护用户结构）
- 🏷️ 标签分类体系

## 📜 许可证

MIT

## 🙏 致谢

- 基于 [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) 构建
- 灵感来自 "本地 Markdown 仓库" 模式
- 参考实现：[arxiv-daily-mcp](https://github.com/nerin81-netizen/arxiv-daily-mcp)

---

> 🌟 如果这个 MCP 帮你管理了本地知识库，给仓库点个 star 吧！
