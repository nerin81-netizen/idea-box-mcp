# 🧠 idea-box-mcp

> **Cherche et sauvegarde tes idées dans des dossiers Markdown locaux avec le langage naturel. Simple comme bonjour.**

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/idea-box-mcp)](https://github.com/nerin81-netizen/idea-box-mcp/stargazers)

**🌍 Lis dans ta langue :** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · **Français** · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

[🚀 Démarrage rapide](#-démarrage-rapide) · [🛠 Outils](#-outils-5) · [🎬 Démo](#-démo) · [🏗 Architecture](#-architecture) · [🧪 Développement](#-développement)

---

## ✨ C'est quoi ça ?

**T'as des dossiers pleins de fichiers Markdown.** Des idées que t'as collectées. Des mémos, des liens, des références. Tu sais qu'ils sont là — mais quand t'en as besoin, comment tu les trouves vite ? C'est ça le problème.

`idea-box-mcp` transforme tes dossiers locaux de Markdown en **outils que ton LLM peut utiliser**. Au lieu de :

```bash
# ❌ Avant : chercher à la main
grep -r "AI" ~/ideas-h/
find ~/memos-h/ -name "*.md" -exec grep -l "arxiv" {} \;
```

Maintenant tu peux dire :

```text
# ✅ Maintenant : langage naturel
"Trouve-moi des idées sur l'IA"
"Montre-moi les mémos arxiv"
"Sauvegarde ça — je lirai ce lien plus tard"
```

**Deux dossiers exposés :**

| Dossier | Ce qu'il y a dedans | Quand tu l'utilises |
|---|---|---|
| `~/ideas-h/` | Idées d'apps avec statut/note | "Je construis quoi ensuite ?" |
| `~/memos-h/` | Références brutes (8 catégories) | "J'ai sauvegardé quoi avant ?" |

> **L'idée centrale :** Tes dossiers locaux de Markdown sont déjà une base de connaissances. Ce MCP les rend juste *consultables* par les LLMs.

## 🛠 Outils (5)

| Outil | Args | Description | Exemple |
|---|---|---|---|
| `search_ideas` | `keyword`, `limit` | Cherche des idées par mot-clé | "Trouve-moi des idées d'IA" |
| `count_ideas` | — | Statistiques (total, par note, récentes) | "J'ai combien d'idées ?" |
| `search_memos` | `keyword`, `category`, `limit` | Cherche des mémos (8 catégories) | "Cherche-moi des mémos arxiv" |
| `count_memos` | — | Statistiques (total, par catégorie) | "Montre-moi les stats du memo-box" |
| `add_memo` | `title`, `content`, `category`, `tags` | Ajoute un mémo avec auto-catégorisation | "Sauvegarde ça — ..." |

### Scénarios réels

**Scénario 1 : "C'était quoi cette idée de health tracking ?"**

Tu te souviens d'avoir écrit un truc sur une app de santé y'a 2 semaines, mais tu la trouves pas. Demande juste :

```text
"Cherche-moi des idées sur la santé"

→ 🔍 Résultats pour 'santé' — 3 sur 145 idées

  · **App de données de santé intégrées** [B]
    Données d'hôpitaux, pharmacies, assurances en un seul endroit...
    📁 `2026-06-15_app-donnees-sante.md`

  · **Alerte médication + interactions**
    App qui vérifie les effets secondaires quand tu prends des médocs...
    📁 `2026-06-20_alerte-medication.md`
```

**Scénario 2 : "Je garde ça pour plus tard"**

Tu navigues et tu trouves un truc intéressant. Au lieu de bookmarker (et d'oublier), dis juste :

```text
"Sauvegarde ça — Tutoriel serving avec vLLM : https://vllm.readthedocs.io/en/latest/
Tags : mlops, inference, vllm"

→ ✅ Sauvegardé : `links/2026-07-06_tutoriel-serving-vllm.md`
   Catégorie : 🔗 Liens
```

Plus tard, tu demandes :

```text
"Cherche-moi des mémos sur l'inference"

→ 🔍 Recherche dans memo-box — 2 sur 11 mémos

  · 🔗 Liens **Tutoriel serving avec vLLM**
    https://vllm.readthedocs.io/en/latest/
    📁 `links/2026-07-06_tutoriel-serving-vllm.md`
```

**Scénario 3 : "J'ai combien d'idées ?"**

```text
"J'ai combien d'idées ?"

→ 📊 État de l'idea-box

📁 Total : 145 idées
🥇 Note S : 0
🥈 Note A : 1
🥉 Note B : 0
⚪ Note C : 0

**5 dernières ajoutées :**
  · 🧠 [Idée récente 1]
  · 📋 [Idée récente 2]
  · 📰 [Idée récente 3]
  · …
```

### `search_ideas(keyword, limit=5)`

Cherche dans les fichiers de l'idea-box par mot-clé dans titre + contenu. Renvoie titre, résumé, note (S/A/B/C) et chemin du fichier.

### `count_ideas()`

Renvoie le total, la distribution des notes (S/A/B/C), et les 5 idées les plus récentes.

### `search_memos(keyword="", category="", limit=10)`

Cherche dans le memo-box. Filtre optionnel par `category` :
`links` · `news` · `quotes` · `references` · `snippets` · `specs` · `tips` · `misc`

### `count_memos()`

Renvoie le total et le détail par catégorie, plus les 3 dernières additions.

### `add_memo(title, content, category="", tags="")`

Ajoute un nouveau mémo. Si `category` est vide, le serveur la détecte automatiquement :
- URLs présentes → `links`
- Code/commandes/configs → `snippets`
- Citations / texte entre guillemets → `quotes`
- Mots-clés d'actualités → `news`
- Specs/besoins → `specs`
- How-to / fixes d'erreurs → `tips`
- Papiers/livres/liens → `references`
- Défaut → `misc`

Renvoie le chemin du fichier et la catégorie détectée.

## 🚀 Démarrage rapide

### Installation

```bash
pip install idea-box-mcp
```

Ou depuis le source :

```bash
git clone https://github.com/nerin81-netizen/idea-box-mcp
cd idea-box-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Configurer les chemins

Par défaut, le serveur lit de :
- Idea-box : `~/ideas-h/`
- Memo-box : `~/memos-h/`

Pour changer, édite les constantes en haut de `server.py` :

```python
IDEA_DIR = Path("/ton/chemin/ideas-h")
MEMO_DIR = Path("/ton/chemin/memos-h")
```

### Enregistre dans ton client MCP

#### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` :

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

`.cursor/mcp.json` :

```json
{
  "mcpServers": {
    "idea-box": {
      "command": "idea-box-mcp"
    }
  }
}
```

## 🎬 Démo

### Chercher des idées

```text
👤 Trouve-moi des idées d'IA

🤖 Claude :
🔍 Résultats pour 'IA' — 139 sur 145 idées

  · **Journal de croissance mentale**
    Une app pour écrire un journal simple et ressentir la croissance mentale jour après jour…
    📁 `2026-06-28_journal-croissance-mentale.md`

  · **Blackbox de poche**
    Un blackbox qui enregistre les conversations de la journée depuis la poche du pantalon…
    📁 `2026-06-28_blackbox-de-poche.md`
```

### Statistiques de l'idea-box

```text
👤 J'ai combien d'idées ?

🤖 Claude :
📊 **État de l'idea-box**

📁 Total : 145 idées
🥇 Note S : 0
🥈 Note A : 1
🥉 Note B : 0
⚪ Note C : 0

**5 dernières :**
  · 🧠 [Titre d'idée récente 1]
  · 📋 [Titre d'idée récente 2]
  · 📰 [Titre d'idée récente 3]
  · …
```

(Les vrais titres dépendent du contenu de ton dossier local `~/ideas-h/`.)

### Ajouter un mémo

```text
👤 Sauvegarde ça — Pattern sécurisé pour push avec GitHub PAT
       export GH_TOKEN=YOUR_TOKEN && git push, puis nettoyer git remote set-url.
       https://github.com/settings/tokens pour révoquer.
       Tags : github, security, mcp-publish

🤖 Claude :
✅ Sauvegardé : `links/2026-07-06_pattern-securise-push-github-pat.md`
   Catégorie : 🔗 Liens
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

**Choix de design :**

- **stdio transport** — standard MCP
- **FastMCP** — SDK Python officiel d'Anthropic
- **Zéro deps externes au-delà de MCP** — pur file I/O
- **Read-only sur idea-box** (préserve ta structure) + **write sur memo-box** (ajoute de nouveaux fichiers)
- **Auto-catégorisation** des mémos avec heuristiques simples (URLs / code / mots-clés)

## 🧪 Développement

```bash
# Installe les dépendances de dev
pip install -e ".[dev]"

# Teste stdio JSON-RPC directement
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | idea-box-mcp

# Test unitaire de la logique de catégorisation
python -c "
from idea_box_mcp.server import _detect_memo_category
print(_detect_memo_category('GitHub PAT', 'export GH_TOKEN=...'))
# → 'links'
print(_detect_memo_category('Bash script', 'pip install mcp'))
# → 'snippets'
"
```

## 🌍 Roadmap

- [x] v0.1.0 — 5 outils, stdio, idea-box + memo-box
- [ ] v0.2.0 — Outil `add_idea` avec prompt de statut/note
- [ ] v0.3.0 — Filtrage par `tags` dans mémos et recherche croisée
- [ ] v0.4.0 — Transitions de statut dans idées (💭 → 🔍 → 💼)
- [ ] v0.5.0 — Répertoires configurables via env vars

## 🤝 Contribuer

Issues et PRs bienvenus. Particulièrement utile :

- 📂 Nouvelles catégories de mémos
- 🔍 Meilleure recherche (ex. fuzzy match, semantic search)
- 📝 Outils d'écriture dans idea-box (avec précaution — préserver la structure utilisateur)
- 🏷️ Taxonomie de tags

## 📜 Licence

MIT

## 🙏 Crédits

- Construit avec [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Inspiré par le pattern "local Markdown vault"
- Implémentation de référence : [arxiv-daily-mcp](https://github.com/nerin81-netizen/arxiv-daily-mcp)

---

> 🌟 Mets une étoile au repo si ce MCP t'a aidé à gérer ta base de connaissances locale.
