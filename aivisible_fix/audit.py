from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import urljoin

from .crawlers import AI_CRAWLERS
from .fetch import fetch
from .robots import agent_status, parse_robots_txt

# Each check's point value. Weighted toward the two things that, per current
# published data, cause the overwhelming majority of AI-search invisibility:
# blocked crawlers and a missing sitemap/structured data trail to follow.
POINTS = {
    "robots_reachable": 5,
    "no_ai_crawlers_blocked": 40,
    "llms_txt_present": 20,
    "sitemap_present": 15,
    "sitemap_referenced_in_robots": 5,
    "structured_data_present": 15,
}


@dataclass
class Finding:
    check: str
    passed: bool
    points: int
    detail: str


@dataclass
class AuditReport:
    base_url: str
    findings: list[Finding] = field(default_factory=list)
    blocked_agents: list[str] = field(default_factory=list)
    score: int = 0

    def add(self, check: str, passed: bool, detail: str) -> None:
        points = POINTS[check] if passed else 0
        self.findings.append(Finding(check, passed, points, detail))
        self.score += points


def run_audit(base_url: str) -> AuditReport:
    base_url = base_url.rstrip("/")
    if not base_url.lower().startswith("https://"):
        raise ValueError(
            f"Refusing to audit '{base_url}': only https:// URLs are supported. "
            "This tool never fetches over plaintext HTTP, for both your safety "
            "and the target site's."
        )
    report = AuditReport(base_url=base_url)

    robots_res = fetch(urljoin(base_url + "/", "robots.txt"))
    if not robots_res.ok:
        report.add("robots_reachable", False, "robots.txt missing or unreachable — AI crawlers default to allowed, but you have no way to signal intent or steer them to a sitemap.")
        groups = []
    else:
        report.add("robots_reachable", True, "robots.txt found.")
        groups = parse_robots_txt(robots_res.text)

    blocked = []
    for agent in AI_CRAWLERS:
        status = agent_status(groups, agent)
        if status == "blocked":
            blocked.append(agent)
    report.blocked_agents = blocked
    if blocked:
        report.add(
            "no_ai_crawlers_blocked",
            False,
            f"{len(blocked)} AI crawler(s) explicitly blocked: {', '.join(blocked)}.",
        )
    else:
        report.add("no_ai_crawlers_blocked", True, "No known AI crawler is explicitly blocked.")

    llms_res = fetch(urljoin(base_url + "/", "llms.txt"))
    report.add(
        "llms_txt_present",
        llms_res.ok and len(llms_res.text.strip()) > 0,
        "llms.txt found." if llms_res.ok else "No /llms.txt — the emerging convention for telling an LLM what your site is and which pages matter most.",
    )

    sitemap_url = None
    m = re.search(r"(?im)^sitemap:\s*(\S+)", robots_res.text) if robots_res.ok else None
    if m:
        sitemap_url = m.group(1).strip()
    sitemap_res = fetch(sitemap_url or urljoin(base_url + "/", "sitemap.xml"))
    sitemap_looks_valid = sitemap_res.ok and ("<urlset" in sitemap_res.text or "<sitemapindex" in sitemap_res.text)
    report.add(
        "sitemap_present",
        sitemap_looks_valid,
        "sitemap.xml found and looks valid." if sitemap_looks_valid else "No reachable/valid sitemap.xml — AI crawlers (and search engines) have no efficient way to discover your full page list.",
    )
    report.add(
        "sitemap_referenced_in_robots",
        m is not None,
        "robots.txt points crawlers at your sitemap." if m else "robots.txt doesn't reference a Sitemap: line, even if sitemap.xml exists at the default path.",
    )

    home_res = fetch(base_url + "/")
    has_jsonld = home_res.ok and bool(re.search(r'<script[^>]+type=["\']application/ld\+json["\']', home_res.text, re.I))
    report.add(
        "structured_data_present",
        has_jsonld,
        "JSON-LD structured data found on the homepage." if has_jsonld else "No JSON-LD structured data on the homepage — AI answer engines lean on schema.org markup to extract facts (org name, product, FAQ, etc.) reliably.",
    )

    return report
