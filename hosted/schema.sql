-- Schema for the (not yet built) hosted-monitoring tier.
-- SQLite-compatible by design: the whole point of this tier is that it
-- should be cheaply self-hostable (a single SQLite file + a cron job is
-- enough for the first ~100 customers) rather than requiring a managed
-- Postgres instance from day one. Written now, ahead of actual demand,
-- so building it later is a data-layer that already exists, not a
-- from-scratch design exercise once the waitlist justifies it.

create table if not exists sites (
    id integer primary key autoincrement,
    url text not null unique,
    owner_email text,               -- who to alert on regression; null until a paid signup exists
    added_at text not null default (datetime('now')),
    check_interval_hours integer not null default 168  -- weekly by default
);

create table if not exists audits (
    id integer primary key autoincrement,
    site_id integer not null references sites(id) on delete cascade,
    score integer not null,
    blocked_agents text,            -- JSON array, e.g. ["GPTBot","ClaudeBot"]
    findings_json text not null,    -- full structured report, for history/diffing
    checked_at text not null default (datetime('now'))
);
create index if not exists idx_audits_site_time on audits(site_id, checked_at);

create table if not exists alerts (
    id integer primary key autoincrement,
    site_id integer not null references sites(id) on delete cascade,
    audit_id integer not null references audits(id) on delete cascade,
    reason text not null,           -- e.g. "score dropped 85 -> 40: GPTBot newly blocked"
    sent_at text,                   -- null until actually delivered
    created_at text not null default (datetime('now'))
);

-- Deliberately no payments/subscriptions table yet: that schema depends on
-- whichever processor ends up used (Stripe customer/subscription IDs, most
-- likely), and shouldn't be guessed at before that account exists.
