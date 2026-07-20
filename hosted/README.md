# hosted/ — not a running service (yet)

This directory holds the data-layer design for the future paid, hosted
monitoring tier described in `LAUNCH.md` and `BUSINESS_PLAN.md`. Nothing in
here runs anywhere right now — there is no server, no deployment, no
account. It exists so that the day real demand shows up (tracked via the
waitlist issue template — see the repo's "New Issue" page), the data model
doesn't need to be designed from scratch under time pressure.

- `schema.sql` — SQLite-first schema (sites, audits, alerts). Cheap enough
  to self-host on a single small VM or even a scheduled GitHub Action
  writing to a committed SQLite file, before ever justifying a managed
  database.
- No payments table on purpose — that shape depends on whichever processor
  ends up used, and shouldn't be guessed at before that account exists.

## Why a "database" isn't running today

Every option for actually hosting this (a VPS, Supabase, Railway, etc.)
needs an account tied to a real identity, the same category of blocker
documented for PyPI and GitHub in `BUSINESS_PLAN.md`. What's genuinely
buildable without one, and what's here instead: the schema itself, and a
zero-infrastructure way to collect real demand signal — GitHub Issues, via
the "Join the hosted-monitoring waitlist" issue template. That's a real,
live, queryable data store (via the GitHub API / issue search) that needed
no new account because the repo already exists.
