# 🧠 idea-box-mcp

> **ローカルの Markdown 知識ベース(idea-box + memo-box)を自然言語で検索・追加できる MCP サーバー。**

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/idea-box-mcp)](https://github.com/nerin81-netizen/idea-box-mcp/stargazers)

**🌍 言語を選ぶ:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

[🚀 クイックスタート](#-クイックスタート) · [🛠 ツール](#-ツール5つ) · [🎬 デモ](#-デモ) · [🏗 アーキテクチャ](#-アーキテクチャ) · [🧪 開発](#-開発)

---

## ✨ これって何？

**君のフォルダには Markdown ファイルが山ほどあるだろ？** 集めたアイデア、メモ、リンク、リファレンス…あるのはわかってるけど、いざ探そうとすると面倒くさい。それを解決するのがこれだよ。

`idea-box-mcp` はローカルの Markdown フォルダを **LLM が直接呼び出せるツール**に変えてくれる。たとえば：

```bash
# ❌ 昔のやり方：手動検索
grep -r "AI" ~/ideas-h/
find ~/memos-h/ -name "*.md" -exec grep -l "arxiv" {} \;
```

今はこんな感じで話しかけるだけ：

```text
# ✅ 新しいやり方：自然言語
"AI 関連のアイデア探して"
"arxiv のメモ見せて"
"メモしといて — このリンクあとで見る"
```

**2つのディレクトリを公開：**

| ディレクトリ | 中身 | いつ使う？ |
|---|---|---|
| `~/ideas-h/` | アプリのアイデア（ステータス/グレード付き） | "次は何作ろう？" |
| `~/memos-h/` | 生のリファレンス（8カテゴリ） | "前に何保存したっけ？" |

> **コアな考え方：** ローカルの Markdown ファイルはすでに知識ベース。この MCP はそれを LLM が *検索可能* にするだけ。

## 🛠 ツール (5つ)

| ツール | 引数 | 説明 | プロンプト例 |
|---|---|---|---|
| `search_ideas` | `keyword`, `limit` | idea-box をキーワード検索 | "AI 関連のアイデア探して" |
| `count_ideas` | — | 統計（合計、グレード別、最近） | "アイデアいくつある？" |
| `search_memos` | `keyword`, `category`, `limit` | memo-box 検索（8カテゴリ） | "arxiv のメモ探して" |
| `count_memos` | — | 統計（合計、カテゴリ別） | "メモボックスの統計見せて" |
| `add_memo` | `title`, `content`, `category`, `tags` | 新規メモ追加（自動カテゴリ分類） | "メモしといて — ..." |

### 実際の使い方

**シナリオ 1: 「あの健康トラッキングのアイデアどこいった？」**

2週間前に健康アプリについて書いたのを覚えてるけど見つからない。そんな時は聞くだけ：

```text
"健康関連のアイデア探して"

→ 🔍 '健康' 検索結果 — 3件 / 全145件

  · **健康データ統合アプリ** [B]
    病院/薬局/保険のデータを一箇所に...
    📁 `2026-06-15_健康データ統合アプリ.md`

  · **服薬アラーム+相互作用チェック**
    薬飲むときに副作用をチェックするアプリ...
    📁 `2026-06-20_服薬アラーム.md`
```

**シナリオ 2: 「あとで見る用に保存しといて」**

ネットサーフィン中に面白いものを見つけた。ブックマークに放り込んで忘れるより、そのまま言っちゃおう：

```text
"メモしといて — vLLM サーブチュートリアル: https://vllm.readthedocs.io/en/latest/
タグ: mlops, inference, vllm"

→ ✅ 保存完了: `links/2026-07-06_vLLM サーブチュートリアル.md`
   カテゴリ: 🔗 リンク
```

あとでこんな風に聞ける：

```text
"inference 関連のメモ探して"

→ 🔍 メモボックス検索 — 2件 / 全11件

  · 🔗 リンク **vLLM サーブチュートリアル**
    https://vllm.readthedocs.io/en/latest/
    📁 `links/2026-07-06_vLLM サーブチュートリアル.md`
```

**シナリオ 3: 「アイデアいくつある？」**

```text
"アイデアいくつある？"

→ 📊 アイデアボックス状況

📁 全 145件
🥇 S グレード: 0件
🥈 A グレード: 1件
🥉 B グレード: 0件
⚪ C グレード: 0件

**最近追加した5件:**
  · 🧠 [最近追加されたアイデアタイトル 1]
  · 📋 [最近追加されたアイデアタイトル 2]
  · 📰 [最近追加されたアイデアタイトル 3]
  · …
```

### `search_ideas(keyword, limit=5)`

idea-box ファイルをキーワードでタイトル＋内容検索。タイトル、要約、グレード(S/A/B/C)、ファイルパスを返す。

### `count_ideas()`

合計数、グレード別分布(S/A/B/C)、最近5件のアイデアを返す。

### `search_memos(keyword="", category="", limit=10)`

memo-box 検索。`category` でフィルタ可能：
`links` · `news` · `quotes` · `references` · `snippets` · `specs` · `tips` · `misc`

### `count_memos()`

合計数＋カテゴリ別統計＋最近3件を返す。

### `add_memo(title, content, category="", tags="")`

新規メモ追加。`category` を空にするとサーバーが自動分類：
- URL あり → `links`
- コード/コマンド/config → `snippets`
- 引用/クォート → `quotes`
- ニュースキーワード → `news`
- スペック/要件 → `specs`
- How-to / エラー解決 → `tips`
- 論文/本/リンク → `references`
- デフォルト → `misc`

ファイルパスと検出されたカテゴリを返す。

## 🚀 クイックスタート

### インストール

```bash
pip install idea-box-mcp
```

またはソースから：

```bash
git clone https://github.com/nerin81-netizen/idea-box-mcp
cd idea-box-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### パス設定

デフォルトでは以下のパスを読み込む：
- Idea-box: `~/ideas-h/`
- Memo-box: `~/memos-h/`

変更するには `server.py` の上部を編集：

```python
IDEA_DIR = Path("/君の/パス/ideas-h")
MEMO_DIR = Path("/君の/パス/memos-h")
```

### MCP クライアントに登録

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

## 🎬 デモ

### アイデア検索

```text
👤 AI 関連のアイデア探して

🤖 Claude:
🔍 'AI' 検索結果 — 139件 / 全145件

  · **心の成長日記**
    毎日簡単な日記を書いて心の成長を実感するアプリ …
    📁 `2026-06-28_心の成長日記.md`

  · **ポケットブラックボックス**
    スマホがポケットの中で一日の会話を録音するブラックボックス …
    📁 `2026-06-28_ポケットブラックボックス.md`
```

### アイデアボックス統計

```text
👤 アイデアいくつある？

🤖 Claude:
📊 **アイデアボックス状況**

📁 全 145件
🥇 S グレード: 0件
🥈 A グレード: 1件
🥉 B グレード: 0件
⚪ C グレード: 0件

**最近追加した5件:**
  · 🧠 [最近追加されたアイデアタイトル 1]
  · 📋 [最近追加されたアイデアタイトル 2]
  · 📰 [最近追加されたアイデアタイトル 3]
  · …
```

（実際のタイトルは君の `~/ideas-h/` ディレクトリの中身によるよ。）

### メモ検索

```text
👤 メモボックスの統計見せて

🤖 Claude:
📊 **メモボックス状況** — 全 11件

  💬 引用/文章: 7件
  🔗 リンク: 2件
  📦 その他: 1件
  🛠️ ティップス/回避策: 1件
```

### メモ追加

```text
👤 メモしといて — GitHub PAT 安全pushパターン
       export GH_TOKEN=YOUR_TOKEN && git push 後 git remote set-url をサニタイズ。
       https://github.com/settings/tokens で revoke。
       タグ: github, security, mcp-publish

🤖 Claude:
✅ 保存完了: `links/2026-07-06_GitHub PAT 安全pushパターン.md`
   カテゴリ: 🔗 リンク
```

## 🏗 アーキテクチャ

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

**設計のポイント：**

- **stdio transport** — MCP 標準
- **FastMCP** — Anthropic 公式 Python SDK
- **外部依存ゼロ**（MCP以外）— 純粋なファイル I/O
- **idea-box は読み取り専用**（構造を保護）+ **memo-box は書き込み可能**（新規ファイル追加）
- **自動カテゴリ分類** — シンプルなヒューリスティック（URL/コード/キーワード）

## 🧪 開発

```bash
# dev 依存関係インストール
pip install -e ".[dev]"

# stdio JSON-RPC を直接テスト
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | idea-box-mcp

# カテゴリ分類ロジックのユニットテスト
python -c "
from idea_box_mcp.server import _detect_memo_category
print(_detect_memo_category('GitHub PAT', 'export GH_TOKEN=...'))
# → 'links'
print(_detect_memo_category('Bash script', 'pip install mcp'))
# → 'snippets'
"
```

## 🌍 ロードマップ

- [x] v0.1.0 — 5ツール、stdio、idea-box + memo-box
- [ ] v0.2.0 — `add_idea` ツール（ステータス/グレードプロンプト付き）
- [ ] v0.3.0 — メモ `tag` フィルタリング＋クロスサーチ
- [ ] v0.4.0 — アイデアステータス遷移 (💭 → 🔍 → 💼)
- [ ] v0.5.0 — 環境変数でディレクトリ設定可能

## 🤝 コントリビュート

Issue/PR 大歓迎。特に助かるもの：

- 📂 新しいメモカテゴリ
- 🔍 より良い検索（fuzzy match、semantic search）
- 📝 idea-box 書き込みツール（慎重に — ユーザー構造を保護）
- 🏷️ タグ分類体系

## 📜 ライセンス

MIT

## 🙏 クレジット

- [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) で構築
- "ローカル Markdown 保管庫" パターンにインスパイア
- 参考実装：[arxiv-daily-mcp](https://github.com/nerin81-netizen/arxiv-daily-mcp)

---

> 🌟 この MCP がローカル知識ベース管理に役立ったら、スターをよろしく！
