from __future__ import annotations

import argparse
import sys
from urllib.parse import urljoin

from .audit import run_audit
from .badge import generate_badge_svg
from .fetch import fetch
from .fix import generate_llms_txt, generate_robots_patch


def cmd_audit(args: argparse.Namespace) -> int:
    try:
        report = run_audit(args.url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    print(f"\nAI-visibility audit for {report.base_url}")
    print(f"Score: {report.score}/100\n")
    for f in report.findings:
        mark = "PASS" if f.passed else "FAIL"
        print(f"  [{mark}] {f.check}: {f.detail}")
    if report.blocked_agents:
        print(f"\nBlocked crawlers: {', '.join(report.blocked_agents)}")
    print()
    return 0 if report.score >= 70 else 1


def cmd_fix(args: argparse.Namespace) -> int:
    try:
        report = run_audit(args.url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    robots_res = fetch(urljoin(report.base_url + "/", "robots.txt"))
    existing = robots_res.text if robots_res.ok else ""

    patched_robots = generate_robots_patch(existing, report)
    robots_out = args.out_robots or "robots.fixed.txt"
    with open(robots_out, "w") as fh:
        fh.write(patched_robots)
    print(f"Wrote {robots_out}")

    if not any(f.check == "llms_txt_present" and f.passed for f in report.findings):
        llms_out = args.out_llms or "llms.txt"
        llms_txt = generate_llms_txt(
            site_name=args.name or report.base_url,
            site_description=args.description or f"{args.name or report.base_url} — description needed, edit this file.",
            key_pages=[],
        )
        with open(llms_out, "w") as fh:
            fh.write(llms_txt)
        print(f"Wrote {llms_out} (starter — edit key pages in before publishing)")

    print("\nReview both files, then deploy them at your site root. Nothing was auto-published.")
    return 0


def cmd_badge(args: argparse.Namespace) -> int:
    try:
        report = run_audit(args.url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    svg = generate_badge_svg(report.score)
    out = args.out or "aivisible-badge.svg"
    with open(out, "w") as fh:
        fh.write(svg)
    print(f"Wrote {out} (score {report.score}/100). Host it yourself and embed:")
    print(f'  <a href="https://example.com"><img src="/aivisible-badge.svg" alt="AI-visible: {report.score}/100"></a>')
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aivisible-fix", description="Audit and fix a site's visibility to AI crawlers/answer engines.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_audit = sub.add_parser("audit", help="Score a site's AI-crawler visibility")
    p_audit.add_argument("url", help="e.g. https://example.com")
    p_audit.set_defaults(func=cmd_audit)

    p_fix = sub.add_parser("fix", help="Generate a patched robots.txt and starter llms.txt")
    p_fix.add_argument("url")
    p_fix.add_argument("--name", help="Site/company name for llms.txt")
    p_fix.add_argument("--description", help="One-line description for llms.txt")
    p_fix.add_argument("--out-robots", help="Output path for patched robots.txt")
    p_fix.add_argument("--out-llms", help="Output path for generated llms.txt")
    p_fix.set_defaults(func=cmd_fix)

    p_badge = sub.add_parser("badge", help="Generate a static embeddable score badge (SVG)")
    p_badge.add_argument("url")
    p_badge.add_argument("--out", help="Output path for the badge SVG")
    p_badge.set_defaults(func=cmd_badge)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
