# 🧠 Idea Box MCP

> **Local Markdown knowledge base (idea-box + memo-box) search and add via natural language.**
> 一个将现有 CLI 工作流封装为 MCP 协议的开源工具。

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)

**🌍 其他语言:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md)

---

## ✨ 这是什么

Local Markdown knowledge base (idea-box + memo-box) search and add via natural language.

> **把 CLI 工作流封装进 MCP,这样你就可以用自然语言从任何 MCP 客户端调用它。**

## 🛠 工具

(请替换为实际工具列表 — 参考示例: https://github.com/nerin81-netizen/arxiv-daily-mcp)

## 🚀 快速开始

### 安装

```bash
pip install idea-box-mcp
```

或从源码安装:

```bash
git clone https://github.com/nerin81-netizen/idea-box-mcp
cd idea-box-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### 注册到 MCP 客户端

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

## 🎬 演示

(请替换为实际演示)

## 🏗 架构

```
LLM 客户端 ←stdio/JSON-RPC→ MCP 服务器 ←urllib→ 外部 API
```

## 🧪 开发

```bash
# 直接测试 stdio JSON-RPC
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | idea-box-mcp
```

## 🌍 路线图

- [x] v0.1.0 — 初始发布
- [ ] v0.2.0 — TODO

## 📜 许可证

MIT

---

> 🌟 如果这个 MCP 帮到了你,请给仓库点个 star。
