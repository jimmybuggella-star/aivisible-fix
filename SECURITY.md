# Security

## Data handling

`aivisible-fix` is a stateless CLI. It does not collect, store, transmit, or
retain any data about the sites it audits or the people running it — every
run is local: fetch a few public URLs (`robots.txt`, `llms.txt`,
`sitemap.xml`, the homepage), score them, optionally write output files to
disk. Nothing phones home. There is no server component, no telemetry, no
account, and nothing to breach because there is no data store.

## Transport

- Every network fetch is **HTTPS-only** (`aivisible_fix/fetch.py` rejects
  any `http://` URL outright, and `run_audit()` rejects a non-`https://`
  target before doing anything else). The tool will never make or relay a
  plaintext request.
- The `fix` command never auto-publishes anything — it writes plain files to
  local disk for you to review and deploy yourself, over whatever
  encrypted channel you already use to manage your own site (git push,
  SFTP, your host's dashboard, etc.).

## If a future hosted/paid tier is built

None of the following exists yet — flagging the bar it needs to clear before
it does, since a hosted service does hold customer data (site URLs, an
account, billing):

- TLS in transit (HTTPS everywhere, HSTS) — non-negotiable, no exceptions.
- Encryption at rest for anything stored (audit history, account records) —
  e.g. Postgres with disk-level encryption plus column-level encryption for
  anything sensitive, comparable to how secrets are already handled via
  Supabase Vault elsewhere in this operator's other projects rather than
  ever committed in plaintext.
- No long-lived plaintext API keys/tokens in the codebase — short-lived
  tokens or a secrets manager, full stop.

## Reporting a vulnerability

This is an early-stage, unfunded open-source project with no dedicated
security contact yet. Until one exists, please open a GitHub issue marked
clearly as a security report, or — for anything sensitive enough that a
public issue is a bad idea — hold off on public disclosure and note that in
the issue title so it can be triaged privately first.
