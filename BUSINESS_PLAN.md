# aivisible-fix — business plan

Built independently, from scratch, with no dependency on any existing
project or account — a fresh venture per the operator brief's "research
and build something of your own" instruction.

## Opportunity scoring

| Criterion | Score (1-5) | Notes |
|---|---|---|
| Startup cost | 5 | $0 — stdlib-only Python, no infra required to build/run the core CLI. |
| Time to first revenue | 3 | Free CLI can ship to GitHub/PyPI immediately; a paid tier (hosted monitoring, GitHub App) needs a payment processor — a human step. |
| Automation potential | 5 | The audit + fix logic is fully deterministic and scriptable; a hosted version needs zero manual intervention per customer. |
| Competition | 2 | The "checker" layer is crowded (8-10 free tools found in market research: isvisible.ai, llmpulse.ai, siftly.ai, ai-visibility-checker.io, seoscore.tools, aibotchecker.online, and others). The "auto-fix / auto-PR" layer has no direct competitor found in research as of 2026-07. |
| Scalability | 4 | Same code serves any number of sites; the ceiling is customer acquisition, not engineering. |
| Profit margin | 5 | Near-100% gross margin once hosted — it's compute-light HTTP fetches and text generation, no per-customer human labor. |
| Defensibility | 3 | Moat is being first to ship the auto-fix/auto-PR workflow well and keeping the crawler list current — not a deep technical moat, but a real head start. |

**Overall: proceed, but positioned on the auto-fix angle, not the audit-score angle**, since the latter is already commoditized and given away free by well-funded competitors.

## What exists today (this delivery)

- `aivisible_fix/` — working Python package: `audit` (scores a live URL against 6 checks) and `fix` (generates a patched `robots.txt` and starter `llms.txt`, writes to local files, never auto-publishes).
- Smoke-tested against two real, live sites (example.com — clean-slate site with no signals; nytimes.com — confirmed detection of NYT's known blanket AI-crawler block).
- MIT-licensed, zero dependencies, packaged with `pyproject.toml` for `pip install`.

## Go-to-market

1. **Free CLI + open-source repo** (GitHub/PyPI) — the audit half is commodity, so give it away; it's the acquisition funnel, not the product.
2. **Content**: a handful of posts naming specific well-known sites' AI-crawler blocking status (like the NYT example this tool already surfaces) tend to get shared — this is the same mechanic that made "isvisible.ai" and its peers get initial traction, per the market research pulled during scoping.
3. **Paid tier**: hosted continuous monitoring (re-run weekly, alert on regression) + a GitHub App that opens the fix as a pull request automatically, similar to Dependabot. Target price based on comparable dev-tool SaaS: $9-29/mo solo site, $49-99/mo agency plan covering multiple client sites.
4. **Agency channel**: SEO/marketing agencies managing many client sites are a natural wedge — one agency account monitoring 20 client sites is worth more per sale than 20 individual site owners, and matches how the crowded "checker" competitors are already positioning (agency/dashboard tiers).

## What requires a human (blocked, cannot be done autonomously)

These are the literal blockers per the operating brief's own exception list — flagging them, not stalling on them:

1. **PyPI account** (`pip install aivisible-fix` by name) — account creation.
2. **GitHub App registration** for the auto-PR feature — ties to a GitHub account/identity.
3. **Payment processor** (Stripe or similar) for the paid monitoring tier — payment authorization + business/tax identity.
4. **Domain + hosting account** for a marketing site / hosted dashboard — account creation, plausibly a small recurring cost.
5. **A place to publish the free CLI publicly** — this was built in an isolated sandbox with no independent hosting account; it needs *some* human-owned account to go live anywhere (GitHub, PyPI, npm, etc.). There is no way to make software "live on the internet" with truly zero human-linked identity — publishing always resolves to some account, somewhere. That's a real, structural limit of "zero human involvement," not a gap in effort.

## Ranked next actions once unblocked

1. Publish the repo publicly (GitHub) under a new, dedicated account/org — highest leverage, lowest cost, immediate distribution.
2. Add the "known crawler list" as a small versioned JSON file with a changelog, so re-running old audits stays meaningfully current — the single biggest risk to the tool's credibility is a stale crawler list.
3. Build the GitHub Action wrapper (`aivisible-fix audit` as a CI check that fails a build on regression) — an easy, high-value add given the CLI already exists, no new account needed to build it (only to distribute it via the GitHub Marketplace).
4. Only then build the hosted/paid tier — validate real demand from the free tool's usage/stars before investing in billing infrastructure.

## Lesson learned this session

Initial idea (a basic AI-visibility *score checker*) looked promising until
a first web-research pass surfaced roughly ten existing free competitors —
a five-minute check that avoided building a commodity feature no one would
pay for. The pivot to "audit *and fix*, not just score" is the part of this
space that current market research did not surface any direct competitor
for.
