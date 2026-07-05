# 🧠 Idea Box MCP

> **Local Markdown knowledge base (idea-box + memo-box) search and add via natural language.**
> 既存の CLI ワークフローを MCP にラップしたオープンソース。

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)

**🌍 他の言語で読む:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md)

---

## ✨ これは何?

Local Markdown knowledge base (idea-box + memo-box) search and add via natural language.

> **CLI ワークフローを MCP でラップして、自然言語で呼び出せるようにする。**

## 🛠 ツール

(実際のツール一覧に置き換えてください — 例: https://github.com/nerin81-netizen/arxiv-daily-mcp)

## 🚀 クイックスタート

### インストール

```bash
pip install idea-box-mcp
```

またはソースから:

```bash
git clone https://github.com/nerin81-netizen/idea-box-mcp
cd idea-box-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### MCP クライアントに登録

#### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "idea-box-mcp": {
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
    "idea-box-mcp": {
      "command": "idea-box-mcp"
    }
  }
}
```

## 🎬 デモ

(実際のデモに置き換えてください)

## 🏗 アーキテクチャ

```
LLM クライアント ←stdio/JSON-RPC→ MCP サーバー ←urllib→ 外部 API
```

## 🧪 開発

```bash
# stdio JSON-RPC を直接テスト
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | idea-box-mcp
```

## 🌍 ロードマップ

- [x] v0.1.0 — 初回リリース
- [ ] v0.2.0 — TODO

## 📜 ライセンス

MIT

---

> 🌟 この MCP が役に立ったら、スターを付けてください。
