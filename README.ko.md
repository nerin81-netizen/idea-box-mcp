# 🧠 idea-box-mcp

> **로컬 Markdown 지식창고(idea-box + memo-box)를 자연어로 검색하고 추가하는 MCP 서버.**

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/idea-box-mcp)](https://github.com/nerin81-netizen/idea-box-mcp/stargazers)

**🌍 언어 선택:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

[🚀 빠른 시작](#-빠른-시작) · [🛠 도구](#-도구-5개) · [🎬 데모](#-데모) · [🏗 아키텍처](#-아키텍처) · [🧪 개발](#-개발)

---

## ✨ 이게 뭐하는 거야?

**너 폴더에 Markdown 파일 잔뜩 쌓아놨지?** 아이디어, 메모, 링크, 레퍼런스... 다 있는 건 아는데 막상 찾으려면 귀찮잖아. 그 문제를 해결해주는 게 이거야.

`idea-box-mcp`는 너의 로컬 Markdown 폴더를 **LLM이 바로 호출할 수 있는 도구**로 바꿔줘. 예를 들면:

```bash
# ❌ 예전 방식: 일일이 검색
grep -r "AI" ~/ideas-h/
find ~/memos-h/ -name "*.md" -exec grep -l "arxiv" {} \;
```

이제 그냥 이렇게 말하면 돼:

```text
# ✅ 새로운 방식: 자연어
"AI 관련 아이디어 찾아줘"
"arxiv 메모 보여줘"
"메모해 — 이 링크 나중에 봐야 해"
```

**두 개 디렉토리를 제공해:**

| 디렉토리 | 안에 뭐가 있나 | 언제 쓰나 |
|---|---|---|
| `~/ideas-h/` | 앱 아이디어 (등급/상태 포함) | "뭐 만들지?" 고민될 때 |
| `~/memos-h/` | 날것 그대로 레퍼런스 (8개 카테고리) | "아까 뭐 저장했더라?" 할 때 |

> **핵심 철학:** 너의 로컬 Markdown 파일은 이미 지식베이스야. 이 MCP는 그걸 LLM이 *검색 가능*하게 만들어줄 뿐이야.

## 🛠 도구 (5개)

| 도구 | 인자 | 설명 | 예시 프롬프트 |
|---|---|---|---|
| `search_ideas` | `keyword`, `limit` | idea-box 키워드 검색 | "AI 관련 아이디어 찾아줘" |
| `count_ideas` | — | 통계 (전체, 등급별, 최근) | "내 아이디어 몇 개야?" |
| `search_memos` | `keyword`, `category`, `limit` | memo-box 검색 (8개 카테고리) | "arxiv 메모 찾아줘" |
| `count_memos` | — | 통계 (전체, 카테고리별) | "메모박스 통계 보여줘" |
| `add_memo` | `title`, `content`, `category`, `tags` | 새 메모 추가 (자동 카테고리 분류) | "메모해 — ..." |

### 실제 사용 예시

**시나리오 1: "건강 관련 아이디어 어디 갔지?"**

2주 전에 건강 앱에 대해 뭔가 적었던 게 기억나는데 안 보일 때. 그냥 물어봐:

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

**시나리오 2: "나중에 볼 거 저장해둬"**

웹서핑 하다가 재밌는 거 찾았을 때. 북마크에 박아놓고 까먹지 말고 그냥 말해:

```text
"메모해 — vLLM 서빙 튜토리얼: https://vllm.readthedocs.io/en/latest/
태그: mlops, inference, vllm"

→ ✅ 저장 완료: `links/2026-07-06_vLLM 서빙 튜토리얼.md`
   카테고리: 🔗 링크
```

나중에 이렇게 물어보면:

```text
"inference 관련 메모 찾아줘"

→ 🔍 메모박스 검색 — 2건 / 전체 11개

  · 🔗 링크 **vLLM 서빙 튜토리얼**
    https://vllm.readthedocs.io/en/latest/
    📁 `links/2026-07-06_vLLM 서빙 튜토리얼.md`
```

**시나리오 3: "아이디어 몇 개나 있어?"**

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

idea-box 파일에서 키워드로 제목+내용 검색. 제목, 요약, 등급(S/A/B/C), 파일 경로 반환.

### `count_ideas()`

전체 개수, 등급별 분포(S/A/B/C), 최근 5개 아이디어 반환.

### `search_memos(keyword="", category="", limit=10)`

memo-box 검색. `category`로 필터 가능:
`links` · `news` · `quotes` · `references` · `snippets` · `specs` · `tips` · `misc`

### `count_memos()`

전체 개수 + 카테고리별 통계 + 최근 3개 반환.

### `add_memo(title, content, category="", tags="")`

새 메모 추가. `category` 비우면 서버가 자동 분류해:
- URL 포함 → `links`
- 코드/명령어/config → `snippets`
- 인용문/따옴표 → `quotes`
- 뉴스 키워드 → `news`
- 스펙/요구사항 → `specs`
- How-to / 에러 해결 → `tips`
- 논문/책/링크 → `references`
- 그 외 → `misc`

파일 경로와 감지된 카테고리를 반환.

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

### 경로 설정

기본값으로 서버는 다음 경로를 읽어:
- Idea-box: `~/ideas-h/`
- Memo-box: `~/memos-h/`

변경하려면 `server.py` 상단에서 수정:

```python
IDEA_DIR = Path("/네/경로/ideas-h")
MEMO_DIR = Path("/네/경로/memos-h")
```

### MCP 클라이언트에 등록

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

## 🎬 데모

### 아이디어 검색

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

### 아이디어 박스 통계

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

(실제 제목은 너의 `~/ideas-h/` 폴더 내용에 따라 달라져.)

### 메모 검색

```text
👤 메모박스 통계 보여줘

🤖 Claude:
📊 **메모박스 현황** — 총 11개

  💬 인용/문장: 7개
  🔗 링크: 2개
  📦 기타: 1개
  🛠️ 팁/워크어라운드: 1개
```

### 메모 추가

```text
👤 메모해 — GitHub PAT 안전 push 패턴
       export GH_TOKEN=YOUR_TOKEN && git push 후 git remote set-url 살균.
       https://github.com/settings/tokens 에서 revoke.
       태그: github, security, mcp-publish

🤖 Claude:
✅ 저장 완료: `links/2026-07-06_GitHub PAT 안전 push 패턴.md`
   카테고리: 🔗 링크
```

## 🏗 아키텍처

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

**핵심 설계 결정:**

- **stdio transport** — MCP 표준
- **FastMCP** — Anthropic 공식 Python SDK
- **외부 의존성 제로** (MCP 빼고) — 순수 file I/O
- **idea-box는 읽기 전용** (구조 보존) + **memo-box는 쓰기 가능** (새 파일 추가)
- **자동 카테고리 분류** — 간단한 휴리스틱 (URL / 코드 / 키워드)

## 🧪 개발

```bash
# dev 의존성 설치
pip install -e ".[dev]"

# stdio JSON-RPC 직접 테스트
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | idea-box-mcp

# 카테고리 분류 로직 단위 테스트
python -c "
from idea_box_mcp.server import _detect_memo_category
print(_detect_memo_category('GitHub PAT', 'export GH_TOKEN=...'))
# → 'links'
print(_detect_memo_category('Bash script', 'pip install mcp'))
# → 'snippets'
"
```

## 🌍 로드맵

- [x] v0.1.0 — 5개 도구, stdio, idea-box + memo-box
- [ ] v0.2.0 — `add_idea` 도구 (상태/등급 프롬프트)
- [ ] v0.3.0 — 메모 `tag` 필터링 + 교차 검색
- [ ] v0.4.0 — 아이디어 상태 전환 (💭 → 🔍 → 💼)
- [ ] v0.5.0 — 환경변수로 디렉토리 설정 가능

## 🤝 기여하기

이슈/PR 환영이야. 특히 도움되는 거:

- 📂 새 메모 카테고리
- 🔍 더 나은 검색 (fuzzy match, semantic search)
- 📝 idea-box 쓰기 도구 (조심히 — 유저 구조 보존)
- 🏷️ 태그 분류 체계

## 📜 라이선스

MIT

## 🙏 크레딧

- [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)로 제작
- "Local Markdown vault" 패턴에서 영감
- 레퍼런스 구현: [arxiv-daily-mcp](https://github.com/nerin81-netizen/arxiv-daily-mcp)

---

> 🌟 이 MCP가 로컬 지식베이스 관리에 도움됐다면 별표 눌러줘!
