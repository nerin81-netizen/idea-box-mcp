# 🧠 idea-box-mcp

> **Buscá y guardá tus ideas en carpetas locales de Markdown con lenguaje natural. Así de simple.**

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/idea-box-mcp)](https://github.com/nerin81-netizen/idea-box-mcp/stargazers)

**🌍 Leé en tu idioma:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · **Español** · [Français](README.fr.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

[🚀 Inicio rápido](#-inicio-rápido) · [🛠 Herramientas](#-herramientas-5) · [🎬 Demo](#-demo) · [🏗 Arquitectura](#-arquitectura) · [🧪 Desarrollo](#-desarrollo)

---

## ✨ ¿Qué es esto?

**Tenés carpetas llenas de archivos Markdown.** Ideas que fuiste juntando. Memos, links, referencias. Sabés que están ahí — pero cuando los necesitás, ¿cómo los encontrás rápido? Ese es el problema.

`idea-box-mcp` convierte tus carpetas locales de Markdown en **herramientas que tu LLM puede usar**. En vez de:

```bash
# ❌ Antes: buscar a mano
grep -r "AI" ~/ideas-h/
find ~/memos-h/ -name "*.md" -exec grep -l "arxiv" {} \;
```

Ahora podés decir:

```text
# ✅ Ahora: lenguaje natural
"Buscame ideas sobre AI"
"Mostrame memos de arxiv"
"Guardá esto — este link lo leo después"
```

**Dos carpetas expuestas:**

| Carpeta | Qué hay adentro | Cuándo lo usás |
|---|---|---|
| `~/ideas-h/` | Ideas de apps con estado/nota | "¿Qué armo ahora?" |
| `~/memos-h/` | Referencias crudas (8 categorías) | "¿Qué guardé antes?" |

> **La idea central:** Tus carpetas locales de Markdown ya son una base de conocimiento. Este MCP solo las hace *consultables* por LLMs.

## 🛠 Herramientas (5)

| Herramienta | Args | Descripción | Ejemplo |
|---|---|---|---|
| `search_ideas` | `keyword`, `limit` | Buscá ideas por palabra clave | "Buscame ideas de AI" |
| `count_ideas` | — | Estadísticas (total, por nota, recientes) | "¿Cuántas ideas tengo?" |
| `search_memos` | `keyword`, `category`, `limit` | Buscá memos (8 categorías) | "Buscame memos de arxiv" |
| `count_memos` | — | Estadísticas (total, por categoría) | "Mostrame stats del memo-box" |
| `add_memo` | `title`, `content`, `category`, `tags` | Agregá un memo con auto-categorización | "Guardá esto — ..." |

### Escenarios reales

**Escenario 1: "¿Qué era esa idea del health tracking?"**

Te acordás de haber escrito algo sobre una app de salud hace 2 semanas, pero no la encontrás. Solo preguntá:

```text
"Buscame ideas sobre salud"

→ 🔍 Resultados para 'salud' — 3 de 145 ideas

  · **App de datos de salud integrados** [B]
    Datos de hospitales, farmacias, seguros en un solo lugar...
    📁 `2026-06-15_app-datos-salud.md`

  · **Alerta de medicación + interacciones**
    App que checkea efectos secundarios al tomar pastillas...
    📁 `2026-06-20_alerta-medicacion.md`
```

**Escenario 2: "Guardo esto para después"**

Estás navegando y encontrás algo interesante. En vez de bookmarkear (y olvidarte), solo decí:

```text
"Guardá esto — Tutorial de serving con vLLM: https://vllm.readthedocs.io/en/latest/
Tags: mlops, inference, vllm"

→ ✅ Guardado: `links/2026-07-06_tutorial-serving-vllm.md`
   Categoría: 🔗 Links
```

Después preguntás:

```text
"Buscame memos sobre inference"

→ 🔍 Búsqueda en memo-box — 2 de 11 memos

  · 🔗 Links **Tutorial de serving con vLLM**
    https://vllm.readthedocs.io/en/latest/
    📁 `links/2026-07-06_tutorial-serving-vllm.md`
```

**Escenario 3: "¿Cuántas ideas tengo?"**

```text
"¿Cuántas ideas tengo?"

→ 📊 Estado del idea-box

📁 Total: 145 ideas
🥇 Nota S: 0
🥈 Nota A: 1
🥉 Nota B: 0
⚪ Nota C: 0

**Últimas 5 agregadas:**
  · 🧠 [Idea reciente 1]
  · 📋 [Idea reciente 2]
  · 📰 [Idea reciente 3]
  · …
```

### `search_ideas(keyword, limit=5)`

Busca en archivos del idea-box por keyword en título + contenido. Devuelve título, resumen, nota (S/A/B/C) y path del archivo.

### `count_ideas()`

Devuelve total, distribución de notas (S/A/B/C), y las 5 ideas más recientes.

### `search_memos(keyword="", category="", limit=10)`

Busca en el memo-box. Filtro opcional por `category`:
`links` · `news` · `quotes` · `references` · `snippets` · `specs` · `tips` · `misc`

### `count_memos()`

Devuelve total y desglose por categoría, más las 3 últimas adiciones.

### `add_memo(title, content, category="", tags="")`

Agrega un memo nuevo. Si `category` está vacío, el servidor la detecta automáticamente:
- URLs presentes → `links`
- Código/comandos/configs → `snippets`
- Citas / texto entrecomillado → `quotes`
- Palabras clave de noticias → `news`
- Specs/requerimientos → `specs`
- How-to / fixes de errores → `tips`
- Papers/libros/links → `references`
- Default → `misc`

Devuelve el path del archivo y la categoría detectada.

## 🚀 Inicio rápido

### Instalación

```bash
pip install idea-box-mcp
```

O desde el source:

```bash
git clone https://github.com/nerin81-netizen/idea-box-mcp
cd idea-box-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Configurar paths

Por default, el servidor lee de:
- Idea-box: `~/ideas-h/`
- Memo-box: `~/memos-h/`

Para cambiarlo, editá las constantes al inicio de `server.py`:

```python
IDEA_DIR = Path("/tu/path/ideas-h")
MEMO_DIR = Path("/tu/path/memos-h")
```

### Registrá en tu cliente MCP

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

### Buscar ideas

```text
👤 Buscame ideas de AI

🤖 Claude:
🔍 Resultados para 'AI' — 139 de 145 ideas

  · **Diario de crecimiento mental**
    Una app para escribir un diario simple y sentir el crecimiento mental día a día…
    📁 `2026-06-28_diario-crecimiento-mental.md`

  · **Blackbox de bolsillo**
    Un blackbox que graba las conversaciones del día desde el bolsillo del pantalón…
    📁 `2026-06-28_blackbox-de-bolsillo.md`
```

### Estadísticas del idea-box

```text
👤 ¿Cuántas ideas tengo?

🤖 Claude:
📊 **Estado del idea-box**

📁 Total: 145 ideas
🥇 Nota S: 0
🥈 Nota A: 1
🥉 Nota B: 0
⚪ Nota C: 0

**Últimas 5:**
  · 🧠 [Título de idea reciente 1]
  · 📋 [Título de idea reciente 2]
  · 📰 [Título de idea reciente 3]
  · …
```

(Los títulos reales dependen del contenido de tu carpeta local `~/ideas-h/`.)

### Agregar un memo

```text
👤 Guardá esto — Patrón seguro para push con GitHub PAT
       export GH_TOKEN=YOUR_TOKEN && git push, luego limpiar git remote set-url.
       https://github.com/settings/tokens para revocar.
       Tags: github, security, mcp-publish

🤖 Claude:
✅ Guardado: `links/2026-07-06_patron-seguro-push-github-pat.md`
   Categoría: 🔗 Links
```

## 🏗 Arquitectura

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

**Decisiones de diseño:**

- **stdio transport** — estándar MCP
- **FastMCP** — SDK oficial de Python de Anthropic
- **Zero deps externas más allá de MCP** — puro file I/O
- **Read-only en idea-box** (preserva tu estructura) + **write en memo-box** (agrega archivos nuevos)
- **Auto-categorización** de memos con heurísticas simples (URLs / código / keywords)

## 🧪 Desarrollo

```bash
# Instalá dependencias de dev
pip install -e ".[dev]"

# Testeo stdio JSON-RPC directo
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | idea-box-mcp

# Test unitario de la lógica de categorización
python -c "
from idea_box_mcp.server import _detect_memo_category
print(_detect_memo_category('GitHub PAT', 'export GH_TOKEN=...'))
# → 'links'
print(_detect_memo_category('Bash script', 'pip install mcp'))
# → 'snippets'
"
```

## 🌍 Roadmap

- [x] v0.1.0 — 5 herramientas, stdio, idea-box + memo-box
- [ ] v0.2.0 — Herramienta `add_idea` con prompt de estado/nota
- [ ] v0.3.0 — Filtrado por `tags` en memos y búsqueda cruzada
- [ ] v0.4.0 — Transiciones de estado en ideas (💭 → 🔍 → 💼)
- [ ] v0.5.0 — Directorios configurables via env vars

## 🤝 Contribuir

Issues y PRs bienvenidos. Especialmente útil:

- 📂 Nuevas categorías de memos
- 🔍 Mejor búsqueda (ej. fuzzy match, semantic search)
- 📝 Herramientas de escritura en idea-box (con cuidado — preservar estructura del usuario)
- 🏷️ Taxonomía de tags

## 📜 Licencia

MIT

## 🙏 Créditos

- Construido con [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Inspirado en el patrón "local Markdown vault"
- Implementación de referencia: [arxiv-daily-mcp](https://github.com/nerin81-netizen/arxiv-daily-mcp)

---

> 🌟 Dale una estrella al repo si este MCP te ayudó a manejar tu base de conocimiento local.
