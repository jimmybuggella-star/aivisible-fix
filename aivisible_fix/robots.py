"""Minimal robots.txt parser that groups directives by user-agent.

Deliberately not using urllib.robotparser: that API answers "can THIS
one agent fetch THIS one URL", but an audit needs to enumerate, for every
known AI crawler, whether it has its own group and whether that group (or
the wildcard group) disallows the whole site.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Group:
    agents: list[str] = field(default_factory=list)
    disallow: list[str] = field(default_factory=list)
    allow: list[str] = field(default_factory=list)


def parse_robots_txt(text: str) -> list[Group]:
    groups: list[Group] = []
    current: Group | None = None
    seen_directive_since_agent = True  # forces first "User-agent" to start a group

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field_name, _, value = line.partition(":")
        field_name = field_name.strip().lower()
        value = value.strip()

        if field_name == "user-agent":
            if current is None or not seen_directive_since_agent:
                current = Group()
                groups.append(current)
            current.agents.append(value)
            seen_directive_since_agent = False
        elif field_name == "disallow" and current is not None:
            current.disallow.append(value)
            seen_directive_since_agent = True
        elif field_name == "allow" and current is not None:
            current.allow.append(value)
            seen_directive_since_agent = True
        # sitemap / crawl-delay / other fields intentionally ignored here;
        # sitemap presence is checked separately by audit.py.

    return groups


def blocks_everything(group: Group) -> bool:
    """True if this group disallows the whole site and doesn't carve out
    an override Allow for it (Allow: / or Allow: with empty/root path)."""
    has_blanket_disallow = any(d.strip() == "/" for d in group.disallow)
    if not has_blanket_disallow:
        return False
    has_override_allow = any(a.strip() == "/" for a in group.allow)
    return not has_override_allow


def agent_status(groups: list[Group], agent: str) -> str:
    """Return 'blocked', 'allowed-explicit', or 'allowed-default' for one AI agent.

    'allowed-default' means the site has no group naming this agent and no
    wildcard (*) group blocking everything — the crawler is free to fetch
    under robots.txt's default-allow behaviour, but the site owner never
    made an explicit decision either way.
    """
    agent_lower = agent.lower()
    named_group = next(
        (g for g in groups if any(a.lower() == agent_lower for a in g.agents)),
        None,
    )
    if named_group is not None:
        return "blocked" if blocks_everything(named_group) else "allowed-explicit"

    wildcard_group = next((g for g in groups if "*" in g.agents), None)
    if wildcard_group is not None and blocks_everything(wildcard_group):
        return "blocked"
    return "allowed-default"
