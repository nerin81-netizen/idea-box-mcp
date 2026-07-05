# 🧠 idea-box-mcp

> **ابحث واحفظ أفكارك في مجلدات Markdown المحلية باستخدام اللغة الطبيعية. ببساطة كده.**

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/nerin81-netizen/idea-box-mcp)](https://github.com/nerin81-netizen/idea-box-mcp/stargazers)

**🌍 اقرأ بلغتك:** [English](README.md) · [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Français](README.fr.md) · [हिन्दी](README.hi.md) · **العربية**

[🚀 البدء السريع](#-البدء-السريع) · [🛠 الأدوات](#-الأدوات-5) · [🎬 العرض التوضيحي](#-العرض-التوضيحي) · [🏗 البنية](#-البنية) · [🧪 التطوير](#-التطوير)

---

## ✨ ما هذا؟

**عندك مجلدات مليانة ملفات Markdown.** أفكار جمعتها. مذكرات، روابط، مراجع. عارف إنها موجودة — بس لما تحتاجها، تلاقيها بسرعة إزاي؟ دي المشكلة.

`idea-box-mcp` بيحول مجلدات Markdown المحلية عندك إلى **أدوات يقدر الـ LLM يستعملها**. بدل:

```bash
# ❌ قبل: البحث يدوياً
grep -r "AI" ~/ideas-h/
find ~/memos-h/ -name "*.md" -exec grep -l "arxiv" {} \;
```

دلوقتي تقدر تقول:

```text
# ✅ دلوقتي: لغة طبيعية
"دورلي على أفكار عن AI"
"وريني مذكرات arxiv"
"احفظ ده — هقرا اللينك ده بعدين"
```

**مجلدين معرضين:**

| المجلد | إيه اللي جواه | إمتى تستخدمه |
|---|---|---|
| `~/ideas-h/` | أفكار تطبيقات مع حالة/تقييم | "هعمل إيه بعد كده؟" |
| `~/memos-h/` | مراجع خام (8 تصنيفات) | "حفظت إيه قبل كده؟" |

> **الفكرة الأساسية:** مجلدات Markdown المحلية عندك بالفعل قاعدة معرفة. الـ MCP ده بيخليها بس *قابلة للاستعلام* من الـ LLMs.

## 🛠 الأدوات (5)

| الأداة | المعاملات | الوصف | مثال |
|---|---|---|---|
| `search_ideas` | `keyword`, `limit` | ابحث عن أفكار بالكلمة المفتاحية | "دورلي على أفكار AI" |
| `count_ideas` | — | إحصائيات (الإجمالي، حسب التقييم، الأحدث) | "عندي كام فكرة؟" |
| `search_memos` | `keyword`, `category`, `limit` | ابحث في المذكرات (8 تصنيفات) | "دورلي على مذكرات arxiv" |
| `count_memos` | — | إحصائيات (الإجمالي، حسب التصنيف) | "وريني إحصائيات المذكرات" |
| `add_memo` | `title`, `content`, `category`, `tags` | أضف مذكرة جديدة مع تصنيف تلقائي | "احفظ ده — ..." |

### سيناريوهات حقيقية

**السيناريو 1: "كان فيه فكرة عن تتبع الصحة؟"**

فتاكر إنك كتبت حاجة عن تطبيق صحة من أسبوعين، بس مش لاقيه. اسأل بس:

```text
"دورلي على أفكار عن الصحة"

→ 🔍 نتائج 'الصحة' — 3 من 145 فكرة

  · **تطبيق بيانات صحية متكاملة** [B]
    بيانات المستشفيات والصيدليات والتأمين في مكان واحد...
    📁 `2026-06-15_integrated-health-data-app.md`

  · **تنبيه الأدوية + التفاعلات**
    تطبيق يفحص الآثار الجانبية لما تاخد حبوب...
    📁 `2026-06-20_medication-alert.md`
```

**السيناريو 2: "احفظ ده لبعدين"**

بتتصفح ولقيت حاجة مثيرة للاهتمام. بدل ما تحطها في المفضلة (وتنساها)، قول بس:

```text
"احفظ ده — درس تعليمي عن vLLM: https://vllm.readthedocs.io/en/latest/
الوسوم: mlops, inference, vllm"

→ ✅ اتحفظ: `links/2026-07-06_vllm-serving-tutorial.md`
   التصنيف: 🔗 روابط
```

بعدين تسأل:

```text
"دورلي على مذكرات عن inference"

→ 🔍 بحث في صندوق المذكرات — 2 من 11 مذكرة

  · 🔗 روابط **درس تعليمي عن vLLM**
    https://vllm.readthedocs.io/en/latest/
    📁 `links/2026-07-06_vllm-serving-tutorial.md`
```

**السيناريو 3: "عندي كام فكرة؟"**

```text
"عندي كام فكرة؟"

→ 📊 حالة صندوق الأفكار

📁 الإجمالي: 145 فكرة
🥇 تقييم S: 0
🥈 تقييم A: 1
🥉 تقييم B: 0
⚪ تقييم C: 0

**آخر 5 مضافات:**
  · 🧠 [فكرة حديثة 1]
  · 📋 [فكرة حديثة 2]
  · 📰 [فكرة حديثة 3]
  · …
```

### `search_ideas(keyword, limit=5)`

بيبحث في ملفات صندوق الأفكار بالكلمة المفتاحية في العنوان + المحتوى. بيرجع العنوان، الملخص، التقييم (S/A/B/C)، ومسار الملف.

### `count_ideas()`

بيرجع العدد الإجمالي، توزيع التقييمات (S/A/B/C)، وأحدث 5 أفكار.

### `search_memos(keyword="", category="", limit=10)`

بيبحث في صندوق المذكرات. فلتر اختياري حسب `category`:
`links` · `news` · `quotes` · `references` · `snippets` · `specs` · `tips` · `misc`

### `count_memos()`

بيرجع العدد الإجمالي والتفصيل حسب التصنيف، مع آخر 3 إضافات.

### `add_memo(title, content, category="", tags="")`

بيضيف مذكرة جديدة. لو `category` فاضي، السيرفر بيكتشفها تلقائياً:
- فيه URLs → `links`
- كود/أوامر/إعدادات → `snippets`
- اقتباسات / نص مقتبس → `quotes`
- كلمات مفتاحية أخبار → `news`
- مواصفات/متطلبات → `specs`
- How-to / إصلاح أخطاء → `tips`
- أوراق/كتب/روابط → `references`
- الافتراضي → `misc`

بيرجع مسار الملف والتصنيف المكتشف.

## 🚀 البدء السريع

### التثبيت

```bash
pip install idea-box-mcp
```

أو من المصدر:

```bash
git clone https://github.com/nerin81-netizen/idea-box-mcp
cd idea-box-mcp
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### إعداد المسارات

افتراضياً، السيرفر بيقرأ من:
- صندوق الأفكار: `~/ideas-h/`
- صندوق المذكرات: `~/memos-h/`

للتخصيص، عدل الثوابت في أول `server.py`:

```python
IDEA_DIR = Path("/مسارك/ideas-h")
MEMO_DIR = Path("/مسارك/memos-h")
```

### سجل في عميل MCP بتاعك

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

## 🎬 العرض التوضيحي

### ابحث عن الأفكار

```text
👤 دورلي على أفكار AI

🤖 Claude:
🔍 نتائج 'AI' — 139 من 145 فكرة

  · **يوميات النمو الذهني**
    تطبيق لكتابة يوميات بسيطة والإحساس بالنمو الذهني كل يوم…
    📁 `2026-06-28_mental-growth-diary.md`

  · **الصندوق الأسود للجيب**
    صندوق أسود يسجل محادثات اليوم من جيب البنطلون…
    📁 `2026-06-28_pocket-blackbox.md`
```

### إحصائيات صندوق الأفكار

```text
👤 عندي كام فكرة؟

🤖 Claude:
📊 **حالة صندوق الأفكار**

📁 الإجمالي: 145 فكرة
🥇 تقييم S: 0
🥈 تقييم A: 1
🥉 تقييم B: 0
⚪ تقييم C: 0

**آخر 5:**
  · 🧠 [عنوان فكرة حديثة 1]
  · 📋 [عنوان فكرة حديثة 2]
  · 📰 [عنوان فكرة حديثة 3]
  · …
```

(العناوين الفعلية بتعتمد على محتوى مجلد `~/ideas-h/` المحلي عندك.)

### أضف مذكرة

```text
👤 احفظ ده — نمط الدفع الآمن مع GitHub PAT
       export GH_TOKEN=YOUR_TOKEN && git push، وبعدين نظف git remote set-url.
       https://github.com/settings/tokens للإلغاء.
       الوسوم: github, security, mcp-publish

🤖 Claude:
✅ اتحفظ: `links/2026-07-06_github-pat-safe-push-pattern.md`
   التصنيف: 🔗 روابط
```

## 🏗 البنية

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

**خيارات التصميم:**

- **stdio transport** — معيار MCP
- **FastMCP** — SDK Python الرسمي من Anthropic
- **صفر اعتماديات خارجية غير MCP** — file I/O نقي
- **للقراءة فقط على صندوق الأفكار** (بيحافظ على هيكلتك) + **للكتابة على صندوق المذكرات** (بيضيف ملفات جديدة)
- **تصنيف تلقائي** للمذكرات باستخدام heuristic بسيط (URLs / كود / كلمات مفتاحية)

## 🧪 التطوير

```bash
# ثبت اعتماديات التطوير
pip install -e ".[dev]"

# اختبر stdio JSON-RPC مباشرة
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | idea-box-mcp

# اختبار وحدة منطق التصنيف
python -c "
from idea_box_mcp.server import _detect_memo_category
print(_detect_memo_category('GitHub PAT', 'export GH_TOKEN=...'))
# → 'links'
print(_detect_memo_category('Bash script', 'pip install mcp'))
# → 'snippets'
"
```

## 🌍 خارطة الطريق

- [x] v0.1.0 — 5 أدوات، stdio، صندوق الأفكار + صندوق المذكرات
- [ ] v0.2.0 — أداة `add_idea` مع prompt للحالة/التقييم
- [ ] v0.3.0 — فلترة `tags` في المذكرات والبحث المتقاطع
- [ ] v0.4.0 — انتقالات حالة الأفكار (💭 → 🔍 → 💼)
- [ ] v0.5.0 — مجلدات قابلة للتخصيص عبر env vars

## 🤝 المساهمة

Issues و PRs مرحب بيها. مفيد بشكل خاص:

- 📂 تصنيفات جديدة للمذكرات
- 🔍 بحث أفضل (مثل fuzzy match، semantic search)
- 📝 أدوات كتابة في صندوق الأفكار (بحذر — حافظ على هيكل المستخدم)
- 🏷️ تصنيف الوسوم

## 📜 الترخيص

MIT

## 🙏 الفضل

- مبني بـ [Anthropic MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- مستوحى من نمط "local Markdown vault"
- التنفيذ المرجعي: [arxiv-daily-mcp](https://github.com/nerin81-netizen/arxiv-daily-mcp)

---

> 🌟 لو الـ MCP ده ساعدك تدير قاعدة المعرفة المحلية بتاعتك، اعمل نجمة للريبو.
