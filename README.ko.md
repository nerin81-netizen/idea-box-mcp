# 🧠 Idea Box MCP

> **Local Markdown knowledge base (idea-box + memo-box) search and add via natural language.**
> 기존 CLI 워크플로우를 MCP로 감싼 오픈소스.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)

**🌍 다른 언어로 읽기:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md)

---

## ✨ 이게 뭔가요

Local Markdown knowledge base (idea-box + memo-box) search and add via natural language.

> **CLI 워크플로우를 MCP로 감싸서, 자연어로 호출하세요.**

## 🛠 도구

(실제 도구 목록으로 교체하세요 — 예시: https://github.com/nerin81-netizen/arxiv-daily-mcp)

## 🚀 빠른 시작

### 설치

```bash
pip install idea-box-mcp
```

또는 소스에서:

```bash
git clone https://github.com/nerin81-netizen/idea-box-mcp
cd idea-box-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### MCP 클라이언트에 등록

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

## 🎬 데모

(실제 데모로 교체)

## 🏗 아키텍처

```
LLM 클라이언트 ←stdio/JSON-RPC→ MCP 서버 ←urllib→ 외부 API
```

## 🧪 개발

```bash
# stdio JSON-RPC 직접 테스트
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | idea-box-mcp
```

## 🌍 로드맵

- [x] v0.1.0 — 초기 릴리스
- [ ] v0.2.0 — TODO

## 📜 라이선스

MIT

---

> 🌟 이 MCP가 도움이 되었다면 별표를 눌러주세요.
