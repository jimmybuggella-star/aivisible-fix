# aivisible-fix

Audits a website for the specific things that make it invisible to AI
crawlers and AI answer engines (ChatGPT, Claude, Perplexity, Gemini/AI
Overviews, and others) — and, unlike the free "checker" tools already on
the market, **generates the fix**, not just a score.

```
$ aivisible-fix audit https://example.com
AI-visibility audit for https://example.com
Score: 40/100

  [FAIL] robots_reachable: robots.txt missing or unreachable ...
  [PASS] no_ai_crawlers_blocked: No known AI crawler is explicitly blocked.
  [FAIL] llms_txt_present: No /llms.txt ...
  ...

$ aivisible-fix fix https://example.com --name "Example Co" --description "..."
Wrote robots.fixed.txt
Wrote llms.txt
Review both files, then deploy them at your site root. Nothing was auto-published.
```

## What it checks

1. **robots.txt reachable** — the baseline signal every crawler reads first.
2. **No AI crawler is explicitly blocked** — checked per-agent (GPTBot,
   ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-Web, anthropic-ai,
   PerplexityBot, Perplexity-User, Google-Extended, CCBot, Bytespider,
   Amazonbot, Applebot-Extended, cohere-ai, Meta-ExternalAgent, Diffbot,
   YouBot — see `aivisible_fix/crawlers.py`), not just a blanket `Disallow: /`.
3. **llms.txt present** — the emerging convention (llmstxt.org) for a short,
   LLM-readable summary of what a site is and which pages matter.
4. **sitemap.xml present and valid**, and **referenced from robots.txt**.
5. **JSON-LD structured data on the homepage** — what answer engines lean on
   to extract facts (org, product, FAQ, etc.) without guessing from prose.

Score is out of 100, weighted toward the two things that, per current
published research, cause the overwhelming majority of AI-search invisibility:
blocked crawlers (40 pts) and missing discovery trail — sitemap + llms.txt
(40 pts combined).

## Why this instead of the free checkers

Search "AI visibility checker" and you'll find eight-plus free tools
(isvisible.ai, llmpulse.ai, siftly.ai, and others) that already do the
scoring for free — that part of the market is a commodity and not worth
competing on head to head.

None of them **write the fix**. This tool's differentiator is that
`aivisible-fix fix` outputs a ready-to-deploy patched `robots.txt` (every
existing line preserved, blocked AI agents explicitly re-allowed) and a
starter `llms.txt` — output, not just diagnosis. The natural extension
(not built yet — see ROADMAP below) is a GitHub App that opens this as a
pull request automatically, the way Dependabot does for dependency bumps,
plus scheduled re-audits so a clean report doesn't silently rot as new
crawlers ship.

## Badge

```
$ aivisible-fix badge https://example.com
Wrote aivisible-badge.svg (score 40/100). Host it yourself and embed:
  <a href="https://example.com"><img src="/aivisible-badge.svg" alt="AI-visible: 40/100"></a>
```

Static SVG, generated locally — no server or account required. Color tracks
score (red under 50, amber under 80, green at 80+).

## Install

```
pip install aivisible-fix
```

Or from source: `pip install -e .`

## Hosted monitoring — coming if there's demand

The CLI above is free forever. A hosted tier (scheduled re-audits,
regression alerts, an auto-PR when your visibility breaks) is designed
(`hosted/schema.sql`) but not built — it's not worth building before real
demand exists. If you'd use it, [open a waitlist
issue](../../issues/new?template=waitlist.yml) — that's the actual signal
this project is watching.

No dependencies beyond the Python 3.10+ standard library — deliberately, so
it's trivial to also ship as a single-file GitHub Action.

## Status

v0.2 — live on PyPI (`pip install aivisible-fix`), CI auto-publishes new
releases. Tested against live sites (example.com and nytimes.com,
correctly detecting NYT's well-documented blanket block of AI crawlers).
Not yet packaged as a GitHub Action — see BUSINESS_PLAN.md for what's next
and what still needs a human (payment processor for the paid tier).
