# 🧠 idea-box-mcp

> **Search and add to your local Markdown knowledge bases (idea-box + memo-box) with natural language.**

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/idea-box-mcp)](https://github.com/nerin81-netizen/idea-box-mcp/stargazers)

**🌍 Read in your language:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md)

[🚀 Quickstart](#-quickstart) · [🛠 Tools](#-tools-5) · [🎬 Demo](#-demo) · [🏗 Architecture](#-architecture) · [🧪 Development](#-development)

---

## ✨ What this is

**You have folders full of Markdown files.** Ideas you've been collecting. Memos, links, references. You know they're there — but finding the right one when you need it? That's the problem.

`idea-box-mcp` turns your local Markdown folders into **LLM-callable tools**. Instead of:

```bash
# ❌ Before: Manual searching
grep -r "AI" ~/ideas-h/
find ~/memos-h/ -name "*.md" -exec grep -l "arxiv" {} \;
```

You can now say:

```text
# ✅ After: Natural language
"AI 관련 아이디어 찾아줘"
"arxiv 메모 보여줘"
"메모해 — 이 링크 나중에 봐야 해"
```

**Two directories exposed:**

| Directory | What's inside | When you'd use it |
|---|---|---|
| `~/ideas-h/` | App ideas with status/grade | "What should I build next?" |
| `~/memos-h/` | Raw references (8 categories) | "What did I save earlier?" |

> **The core idea:** Your local Markdown folders are already a knowledge base. This MCP just makes them *queryable* by LLMs.

## 🛠 Tools (5)

| Tool | Args | Description | Example prompt |
|---|---|---|---|
| `search_ideas` | `keyword`, `limit` | Search idea-box by keyword | "AI 관련 아이디어 찾아줘" |
| `count_ideas` | — | Statistics (total, by grade, recent) | "내 아이디어 몇 개야?" |
| `search_memos` | `keyword`, `category`, `limit` | Search memo-box (8 categories) | "arxiv 메모 찾아줘" |
| `count_memos` | — | Statistics (total, by category) | "메모박스 통계" |
| `add_memo` | `title`, `content`, `category`, `tags` | Add new memo with auto-categorization | "메모해 — ..." |

### Real-world scenarios

**Scenario 1: "What was that idea about health tracking?"**

You remember writing something about a health app 2 weeks ago, but can't find it. Just ask:

```text
"건강 관련 아이디어 찾아줘"

→ 🔍 '건강' 검색 결과 — 3건 / 전체 145개

  · **건강데이터통합앱** [B]
    병원/약국/보험 데이터를 한 곳에서...
    📁 `2026-06-15_건강데이터통합앱.md`

  · **복약알림+상호작용체크**
    약 먹을 때 부작용 체크하는 앱...
    📁 `2026-06-20_복약알림.md`
```

**Scenario 2: "Save this for later"**

You're browsing and find something interesting. Instead of bookmarking (and forgetting), just say:

```text
"메모해 — vLLM 서빙 튜토리얼: https://vllm.readthedocs.io/en/latest/
태그: mlops, inference, vllm"

→ ✅ 저장 완료: `links/2026-07-06_vLLM 서빙 튜토리얼.md`
   카테고리: 🔗 링크
```

Later, you ask:

```text
"inference 관련 메모 찾아줘"

→ 🔍 메모박스 검색 — 2건 / 전체 11개

  · 🔗 링크 **vLLM 서빙 튜토리얼**
    https://vllm.readthedocs.io/en/latest/
    📁 `links/2026-07-06_vLLM 서빙 튜토리얼.md`
```

**Scenario 3: "How many ideas do I have?"**

```text
"내 아이디어 몇 개야?"

→ 📊 아이디어 박스 현황

📁 총 145개
🥇 S 등급: 0개
🥈 A 등급: 1개
🥉 B 등급: 0개
⚪ C 등급: 0개

**최근 추가 5개:**
  · 🧠 [최근 추가된 아이디어 제목 1]
  · 📋 [최근 추가된 아이디어 제목 2]
  · 📰 [최근 추가된 아이디어 제목 3]
  · …
```

### `search_ideas(keyword, limit=5)`

Searches idea-box files by keyword in title + content. Returns title, summary, grade (S/A/B/C), and file path.

### `count_ideas()`

Returns total count, grade distribution (S/A/B/C), and 5 most recent additions.

### `search_memos(keyword="", category="", limit=10)`

Searches memo-box. Optional `category` filter:
`links` · `news` · `quotes` · `references` · `snippets` · `specs` · `tips` · `misc`

### `count_memos()`

Returns total count and per-category breakdown, plus 3 most recent additions.

### `add_memo(title, content, category="", tags="")`

Adds a new memo. If `category` is empty, the server auto-detects from content:
- URLs present → `links`
- Code/commands/configs → `snippets`
- Citations / quoted text → `quotes`
- News keywords → `news`
- Specs/requirements → `specs`
- How-to / error fixes → `tips`
- Papers/books/links → `references`
- Default → `misc`

Returns the file path and detected category.

## 🚀 Quickstart

### Install

```bash
pip install idea-box-mcp
```

Or from source:

```bash
git clone https://github.com/nerin81-netizen/idea-box-mcp
cd idea-box-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Configure paths

By default, the server reads from:
- Idea-box: `~/ideas-h/`
- Memo-box: `~/memos-h/`

To customize, edit the constants at the top of `server.py`:

```python
IDEA_DIR = Path("/your/path/ideas-h")
MEMO_DIR = Path("/your/path/memos-h")
```

### Register with your MCP client

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

## 🎬 Demo

### Search ideas

```text
👤 AI 관련 아이디어 찾아줘

🤖 Claude:
🔍 'AI' 검색 결과 — 139건 / 전체 145개

  · **마음성장일기**
    매일 간단한 일기를 쓰면서 마음의 성장을 체감하는 앱 …
    📁 `2026-06-28_마음성장일기.md`

  · **주머니블랙박스**
    핸드폰이 주머니 속에서 하루의 대화를 계속 녹음하는 블랙박스 …
    📁 `2026-06-28_주머니블랙박스.md`
```

### Idea-box statistics

```text
👤 내 아이디어 몇 개야?

🤖 Claude:
📊 **아이디어 박스 현황**

📁 총 145개
🥇 S 등급: 0개
🥈 A 등급: 1개
🥉 B 등급: 0개
⚪ C 등급: 0개

**최근 추가 5개:**
  · 🧠 [최근 추가된 아이디어 제목 1]
  · 📋 [최근 추가된 아이디어 제목 2]
  · 📰 [최근 추가된 아이디어 제목 3]
  · …
```

(Actual titles depend on your local `~/ideas-h/` directory contents.)

### Search memos

```text
👤 메모박스 통계

🤖 Claude:
📊 **메모박스 현황** — 총 11개

  💬 인용/문장: 7개
  🔗 링크: 2개
  📦 기타: 1개
  🛠️ 팁/워크어라운드: 1개
```

### Add a memo

```text
👤 메모해 — GitHub PAT 안전 push 패턴
       export GH_TOKEN=YOUR_TOKEN && git push 후 git remote set-url 살균.
       https://github.com/settings/tokens 에서 revoke.
       태그: github, security, mcp-publish

🤖 Claude:
✅ 저장 완료: `links/2026-07-06_GitHub PAT 안전 push 패턴.md`
   카테고리: 🔗 링크
```

## 🏗 Architecture

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

**Key design choices:**

- **stdio transport** — MCP standard
- **FastMCP** — Anthropic's official Python SDK
- **Zero external deps beyond MCP** — pure file I/O
- **Read-only on idea-box** (preserves your structure) + **write on memo-box** (adds new files)
- **Auto-categorization** for memos using simple heuristics (URLs / code / keywords)

## 🧪 Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Test stdio JSON-RPC directly
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | idea-box-mcp

# Unit test the categorization logic
python -c "
from idea_box_mcp.server import _detect_memo_category
print(_detect_memo_category('GitHub PAT', 'export GH_TOKEN=...'))
# → 'links'
print(_detect_memo_category('Bash script', 'pip install mcp'))
# → 'snippets'
"
```

## 🌍 Roadmap

- [x] v0.1.0 — 5 tools, stdio, idea-box + memo-box
- [ ] v0.2.0 — `add_idea` tool with status/grade prompt
- [ ] v0.3.0 — Memo `tag` filtering and cross-search
- [ ] v0.4.0 — Idea status transitions (💭 → 🔍 → 💼)
- [ ] v0.5.0 — Configurable directories via env vars

## 🤝 Contributing

Issues and PRs welcome. Particularly useful:

- 📂 New memo categories
- 🔍 Better search (e.g. fuzzy match, semantic search)
- 📝 Idea-box write tools (carefully — preserve user structure)
- 🏷️ Tag taxonomy

## 📜 License

MIT

## 🙏 Credits

- Built with [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Inspired by the "local Markdown vault" pattern
- Reference implementation: [arxiv-daily-mcp](https://github.com/nerin81-netizen/arxiv-daily-mcp)

---

> 🌟 Star the repo if this MCP helped you manage your local knowledge base.
