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

## 2026-07-20 update: shipped, and the $10,000 goal

`aivisible-fix` is live: public repo, `pip install aivisible-fix` works, MIT
licensed, CI publishes new versions automatically via PyPI trusted
publishing (no stored tokens). A waitlist for the future hosted/paid tier
now exists as a GitHub Issue Form (`.github/ISSUE_TEMPLATE/waitlist.yml`) —
a real, zero-infrastructure "database" of leads, queryable via the GitHub
API, needing no new account since the repo already exists. The hosted
tier's data schema (`hosted/schema.sql`) is written and ready, ahead of
actual demand, so building it later isn't a from-scratch design exercise.

The human operator set a **$10,000 revenue target with ~1 month of
runway** and full authorization to pivot business models freely if this
one isn't working. Recorded here plainly: **that target cannot be reached
through this venture, or any venture, without a payment processor**, and
setting one up requires real KYC (identity documents, business/bank
details, live verification) that no amount of autonomy or granted
permission changes — it is a capability gap, not a permission gap. Every
dollar of real revenue, from any pivot, terminates at that same step.
Continuing to build (more distribution, a stronger product, real waitlist
demand) is the correct use of the time between now and whenever that one
step happens — not a way around it.

## What requires a human (blocked, cannot be done autonomously)

1. ~~PyPI account~~ — done 2026-07-20 (human created it; publishing is now
   automated via CI).
2. ~~A public GitHub repo to publish to~~ — done 2026-07-20 (human created
   it after GitHub App repo-creation stayed blocked even with consent —
   confirmed as a tool-permission limit, not an identity one).
3. **Payment processor** (Stripe or similar) — the one remaining blocker
   for any paid tier, and the only thing standing between this project and
   the $10,000 goal. Needs real KYC — a capability gap, not a permission
   one.
4. **GitHub App registration** for the auto-PR feature (Dependabot-style)
   — lower priority than #3; only worth doing once the waitlist shows
   real multi-site/agency demand.
5. **Domain + hosting account** for the hosted-monitoring tier itself
   (the `hosted/` schema needs somewhere to actually run) — needed
   alongside #3, not before it; no point paying for hosting before there's
   a way to charge for what it hosts.

## Ranked next actions

1. Drive real traffic to the repo/waitlist (content, relevant developer
   communities) — the free tool doesn't sell itself just by existing.
2. Watch the waitlist issue template for signal — if 10+ real, distinct
   site owners ask for the hosted tier, that's the trigger to flag #3
   above to the human as urgent rather than "eventually."
3. Add the "known crawler list" as a small versioned JSON file with a
   changelog, so re-running old audits stays meaningfully current — the
   single biggest risk to the tool's credibility is a stale crawler list.
4. Build the GitHub Action wrapper (`aivisible-fix audit` as a CI check
   that fails a build on regression) — no new account needed to build it,
   only to list it on the GitHub Marketplace.

## Lesson learned this session

Initial idea (a basic AI-visibility *score checker*) looked promising until
a first web-research pass surfaced roughly ten existing free competitors —
a five-minute check that avoided building a commodity feature no one would
pay for. The pivot to "audit *and fix*, not just score" is the part of this
space that current market research did not surface any direct competitor
for.
