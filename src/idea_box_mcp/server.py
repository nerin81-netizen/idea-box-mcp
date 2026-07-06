"""idea-box + memo-box MCP Server

Provides tools to:
- search_ideas: Search idea-box by keyword
- count_ideas: Idea-box statistics (total, by grade, recent)
- search_memos: Search memo-box by keyword (8 categories)
- count_memos: Memo-box statistics
- add_memo: Add new memo with auto-categorization

Transport: stdio (Anthropic MCP standard)
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ── 상수 ──────────────────────────────────────────────
KST = timezone(timedelta(hours=9))
IDEA_DIR = Path(os.getenv("IDEA_BOX_DIR", Path.home() / "ideas-h"))
MEMO_DIR = Path(os.getenv("MEMO_BOX_DIR", Path.home() / "memos-h"))

# 메모박스 8개 카테고리
MEMO_CATEGORIES = {
    "links": "🔗 링크",
    "misc": "📦 기타",
    "news": "📰 뉴스",
    "quotes": "💬 인용/문장",
    "references": "📚 참고자료",
    "snippets": "💻 코드/설정",
    "specs": "📋 명세/스펙",
    "tips": "🛠️ 팁/워크어라운드",
}

# 아이디어 박스 등급 패턴
GRADE_PATTERN = re.compile(r"(?:등급|상태|grade)\s*[:=]\s*([SABC])\b", re.IGNORECASE)
STATUS_PATTERN = re.compile(r"💭|💼|✅|🔍|💎|🚧|⚠️|❌|🥇|🥈|🥉")


# ── FastMCP 서버 ─────────────────────────────────────
mcp = FastMCP(
    "idea-box",
    instructions=(
        "Local Markdown knowledge base MCP server. "
        "Search and add to idea-box (app ideas) and memo-box (raw references). "
        "Use natural language like 'AI 관련 아이디어 찾아줘' or '메모 보여줘'."
    ),
)


# ── 아이디어 박스 헬퍼 ────────────────────────────────
def _list_idea_files() -> list[Path]:
    """index.md / dashboard 제외한 모든 아이디어 파일."""
    if not IDEA_DIR.exists():
        return []
    ignore_names = {"index.md", "대시보드.md", "앱인토스_적합성검토.md"}
    return [
        f for f in IDEA_DIR.glob("*.md")
        if f.name.lower() not in ignore_names
    ]


def _extract_title(content: str, filename: str) -> str:
    """파일에서 제목 추출 (첫 번째 # 헤더)."""
    for line in content.splitlines():
        m = re.match(r"^#\s+(.+)", line.strip())
        if m:
            title = m.group(1).strip()
            # "💡" / "💼" 같은 이모지 prefix 제거
            title = re.sub(r"^[💡💼🔍]+\s*", "", title)
            return title
    return filename.replace(".md", "")


def _extract_first_paragraph(content: str, max_len: int = 120) -> str:
    """첫 번째 단락 추출 (요약용)."""
    lines = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("**") or line.startswith("---"):
            continue
        if line.startswith(">") or line.startswith("-"):
            lines.append(line.lstrip(">- "))
            if sum(len(l) for l in lines) > max_len:
                break
            continue
        lines.append(line)
        if sum(len(l) for l in lines) > max_len:
            break
    text = " ".join(lines)[:max_len]
    return text + ("..." if len(text) >= max_len else "")


def _extract_grade(content: str) -> str | None:
    """본문에서 등급(S/A/B/C) 추출."""
    m = GRADE_PATTERN.search(content)
    return m.group(1).upper() if m else None


# ── 메모박스 헬퍼 ────────────────────────────────────
def _list_memo_files(category: str | None = None) -> list[Path]:
    """메모박스 파일 목록. category 지정 시 해당 카테고리만."""
    if not MEMO_DIR.exists():
        return []
    pattern = f"{category}/*.md" if category else "**/*.md"
    return [
        f for f in MEMO_DIR.glob(pattern)
        if f.name.lower() != "index.md"
    ]


def _detect_memo_category(title: str, content: str) -> str:
    """메모 제목/내용으로 카테고리 자동 추정."""
    text = (title + " " + content[:500]).lower()

    # URL 포함 → links
    if re.search(r"https?://", content[:300]):
        return "links"
    # 코드/설정 키워드
    if re.search(r"```|api[_-]?key|token|password|command|config|env|shell|python|bash", text):
        return "snippets"
    # 뉴스 키워드
    if re.search(r"뉴스|속보|발표|출시|공개|업데이트", text):
        return "news"
    # 인용 패턴
    if re.search(r'^>\s|—|".+"\s*[-—]', content[:500], re.MULTILINE):
        return "quotes"
    # 명세/스펙
    if re.search(r"스펙|명세|요구사항|requirement|spec\.", text):
        return "specs"
    # 팁
    if re.search(r"팁|해결|방법|trick|howto|how to|오류 수정|에러|fix", text):
        return "tips"
    # 참고자료
    if re.search(r"논문|paper|arxiv|도서|책|book|github\.com/.+/.+", text):
        return "references"
    return "misc"


# ── MCP Tools ─────────────────────────────────────────
@mcp.tool(
    annotations={
        "title": "Search App Ideas",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
        "idempotentHint": True,
    }
)
async def search_ideas(keyword: str, limit: int = 5) -> str:
    """Search the idea-box by keyword from idea-box(아이디어박스).

    Args:
        keyword: 검색 키워드 (예: 'AI', '환불', '카페', 'MVP')
        limit: 최대 결과 수 (기본 5)

    Returns:
        매칭된 아이디어 목록 (제목 + 요약)
    """
    keyword_lower = keyword.lower().strip()
    if not keyword_lower:
        return "❌ keyword는 비어 있을 수 없습니다."

    matches = []
    for f in _list_idea_files():
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if keyword_lower in content.lower():
            title = _extract_title(content, f.name)
            summary = _extract_first_paragraph(content)
            grade = _extract_grade(content)
            grade_badge = f" [{grade}]" if grade else ""
            matches.append(f"  · **{title}**{grade_badge}\n    {summary}\n    📁 `{f.name}`")

    if not matches:
        return f"🔍 '{keyword}' 매칭 아이디어 없음 (총 {len(_list_idea_files())}개 중)"

    total = len(_list_idea_files())
    header = f"🔍 **'{keyword}' 검색 결과** — {len(matches)}건 / 전체 {total}개"
    return f"{header}\n\n" + "\n\n".join(matches[:limit])


@mcp.tool(
    annotations={
        "title": "Get App Ideas Statistics",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
        "idempotentHint": True,
    }
)
async def count_ideas() -> str:
    """Get app ideas statistics (total count, by grade, recent additions) from idea-box(아이디어박스)."""
    files = _list_idea_files()
    if not files:
        return "📭 아이디어 박스가 비어있어요."

    total = len(files)
    by_grade: dict[str, int] = {"S": 0, "A": 0, "B": 0, "C": 0}

    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            grade = _extract_grade(content)
            if grade and grade in by_grade:
                by_grade[grade] += 1
        except Exception:
            continue

    # 최근 추가 5개
    recent = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)[:5]
    recent_lines = []
    for f in recent:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            title = _extract_title(content, f.name)
            recent_lines.append(f"  · {title} (`{f.name}`)")
        except Exception:
            continue

    return f"""📊 **아이디어 박스 현황**

📁 총 {total}개
🥇 S 등급: {by_grade['S']}개
🥈 A 등급: {by_grade['A']}개
🥉 B 등급: {by_grade['B']}개
⚪ C 등급: {by_grade['C']}개

**최근 추가 5개:**
{chr(10).join(recent_lines)}
"""


@mcp.tool(
    annotations={
        "title": "Search Memos and References",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
        "idempotentHint": True,
    }
)
async def search_memos(keyword: str = "", category: str = "", limit: int = 10) -> str:
    """Search the memo-box by keyword or category from idea-box(아이디어박스).

    Args:
        keyword: 검색 키워드 (선택, 제목+내용 매칭)
        category: 카테고리 필터 (선택, links|news|quotes|references|snippets|specs|tips|misc)
        limit: 최대 결과 수 (기본 10)

    Returns:
        매칭된 메모 목록
    """
    if category and category not in MEMO_CATEGORIES:
        return f"❌ 알 수 없는 category: {category}\n   가능한 값: {', '.join(MEMO_CATEGORIES.keys())}"

    files = _list_memo_files(category if category else None)
    if not files:
        return f"📭 메모박스 (category={category or 'all'}) 비어있음"

    matches = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if keyword and keyword.lower() not in content.lower():
            continue
        # 카테고리는 디렉토리명에서 추출
        cat = f.parent.name if f.parent != MEMO_DIR else "misc"
        cat_label = MEMO_CATEGORIES.get(cat, cat)
        title = _extract_title(content, f.name)
        summary = _extract_first_paragraph(content, max_len=100)
        matches.append(f"  · {cat_label} **{title}**\n    {summary}\n    📁 `{f.relative_to(MEMO_DIR)}`")

    if not matches:
        return f"🔍 keyword='{keyword}' category='{category or 'all'}' 매칭 메모 없음"

    total = len(files)
    header = f"🔍 **메모박스 검색** — {len(matches)}건 / 전체 {total}개"
    return f"{header}\n\n" + "\n\n".join(matches[:limit])


@mcp.tool(
    annotations={
        "title": "Get Memos Statistics",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
        "idempotentHint": True,
    }
)
async def count_memos() -> str:
    """Get memo-box statistics (total count, by category) from idea-box(아이디어박스)."""
    if not MEMO_DIR.exists():
        return "📭 메모박스 디렉토리 없음"

    files = _list_memo_files()
    by_cat: dict[str, int] = {cat: 0 for cat in MEMO_CATEGORIES}
    for f in files:
        cat = f.parent.name if f.parent != MEMO_DIR else "misc"
        if cat in by_cat:
            by_cat[cat] += 1
        else:
            by_cat["misc"] += 1

    lines = [f"📊 **메모박스 현황** — 총 {len(files)}개\n"]
    for cat, count in sorted(by_cat.items(), key=lambda x: -x[1]):
        if count > 0:
            lines.append(f"  {MEMO_CATEGORIES[cat]}: {count}개")

    # 최근 3개
    recent = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)[:3]
    if recent:
        lines.append("\n**최근 추가 3개:**")
        for f in recent:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                title = _extract_title(content, f.name)
                lines.append(f"  · {title}")
            except Exception:
                continue

    return "\n".join(lines)


@mcp.tool(
    annotations={
        "title": "Add New Memo to Repository",
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": False,
        "idempotentHint": False,
    }
)
async def add_memo(title: str, content: str, category: str = "", tags: str = "") -> str:
    """Add a new memo to the local memo-box repository from idea-box(아이디어박스).

    Args:
        title: 메모 제목
        content: 메모 본문 (있는 그대로 저장됨)
        category: 카테고리 (선택, 비우면 자동 감지). links|news|quotes|references|snippets|specs|tips|misc
        tags: 쉼표 구분 태그 (선택, 예: "ai, saas, directory")

    Returns:
        저장된 파일 경로 + 감지된 카테고리
    """
    if not title.strip():
        return "❌ title은 비어 있을 수 없습니다."

    # 카테고리 결정
    if category and category in MEMO_CATEGORIES:
        cat = category
    else:
        cat = _detect_memo_category(title, content)

    # 태그 처리
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    today = datetime.now(KST).strftime("%Y-%m-%d")
    memo_id = f"memo-{datetime.now(KST).strftime('%Y%m%d-%H%M%S')}"

    # 파일 경로
    cat_dir = MEMO_DIR / cat
    cat_dir.mkdir(parents=True, exist_ok=True)
    safe_title = re.sub(r"[^\w\s가-힣一-鿿ぁ-ヿ\-]", "", title).strip()[:50]
    filename = f"{today}_{safe_title}.md"
    out = cat_dir / filename

    tag_str = ", ".join(f"`{t}`" for t in tag_list) if tag_list else ""
    full_content = f"""# 📌 {title}

**날짜:** {today}
**ID:** {memo_id}
**카테고리:** {MEMO_CATEGORIES[cat]}
{"**태그:** " + tag_str if tag_str else ""}

---

## 원문 (있는 그대로)

{content}

## 🎯 쓰임새 (나중에 어떻게 쓸 수 있나)

_(작성 예정)_
"""
    out.write_text(full_content, encoding="utf-8")
    return f"✅ 저장 완료: `{out.relative_to(MEMO_DIR)}`\n   카테고리: {MEMO_CATEGORIES[cat]}"


# ── 진입점 ───────────────────────────────────────────
def main() -> None:
    import sys
    import os
    if len(sys.argv) > 1 and sys.argv[1] == "sse":
        import uvicorn
        from starlette.applications import Starlette
        from starlette.routing import Mount

        class KakaoProxyMiddleware:
            def __init__(self, app):
                self.app = app
            async def __call__(self, scope, receive, send):
                if scope["type"] in ("http", "websocket"):
                    path = scope.get("path", "")
                    if path.startswith("/mcp"):
                        scope["path"] = path[4:] or "/"
                
                async def custom_send(event):
                    if event["type"] == "http.response.start":
                        headers = event.get("headers", [])
                        new_headers = []
                        for k, v in headers:
                            val_str = v.decode("utf-8", errors="ignore")
                            if "/messages" in val_str and not val_str.startswith("/mcp"):
                                val_str = val_str.replace("/messages", "/mcp/messages")
                                v = val_str.encode("utf-8")
                            new_headers.append((k, v))
                        event["headers"] = new_headers
                    await send(event)
                await self.app(scope, receive, custom_send)

        port = int(os.getenv("PORT", 8000))
        sse_app = mcp.sse_app()
        app = Starlette(routes=[Mount("/", app=sse_app)])
        app.add_middleware(KakaoProxyMiddleware)

        print(f"Starting idea-box SSE Server on port {port} with KakaoProxyMiddleware")
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
