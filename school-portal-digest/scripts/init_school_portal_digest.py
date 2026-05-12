#!/usr/bin/env python3
"""Initialize local state for the school-portal-digest skill.

Creates a private local folder with config/state templates. This script does
not collect credentials, log into portals, or write real family data.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def copy_if_missing(src: Path, dst: Path) -> str:
    if dst.exists():
        return f"exists: {dst}"
    shutil.copyfile(src, dst)
    return f"created: {dst}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create local config/state files for School Portal Digest."
    )
    parser.add_argument(
        "--target",
        default="school-portal",
        help="Local state directory to create. Default: school-portal",
    )
    parser.add_argument("--portal-name", help="Portal name, e.g. ParentSquare", default=None)
    parser.add_argument("--login-url", help="Portal login URL", default=None)
    parser.add_argument("--home-url", help="Portal home URL after login", default=None)
    parser.add_argument(
        "--children",
        help="Comma-separated child labels, e.g. 'Child A,Child B' or initials",
        default=None,
    )
    parser.add_argument(
        "--cadence",
        choices=["on-demand", "post-school-day", "daily", "weekday-morning", "weekly"],
        default="post-school-day",
    )
    parser.add_argument(
        "--auth-mode",
        choices=["browser-session", "official-oauth", "keychain", "env-token", "manual-refresh"],
        default="browser-session",
        help="How scheduled runs should authenticate. No secret values are stored by this script.",
    )
    parser.add_argument(
        "--secret-ref",
        default=None,
        help="Optional local keychain/secret-manager reference name. Do not pass a secret value.",
    )
    parser.add_argument(
        "--delivery-mode",
        choices=["announce", "file-only", "none"],
        default="announce",
    )
    parser.add_argument(
        "--calendar-write-mode",
        choices=["recommend-only", "write-with-confirmation", "write-auto"],
        default="recommend-only",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    assets = skill_dir / "assets"
    target = Path(args.target).expanduser().resolve()
    today = datetime.now().astimezone().strftime("%Y-%m-%d")

    target.mkdir(parents=True, exist_ok=True)
    (target / "calendar").mkdir(exist_ok=True)

    config = load_json(assets / "config.example.json")
    if args.portal_name:
        config["portal"]["name"] = args.portal_name
    if args.login_url:
        config["portal"]["loginUrl"] = args.login_url
    if args.home_url:
        config["portal"]["homeUrl"] = args.home_url
    if args.children:
        children = [c.strip() for c in args.children.split(",") if c.strip()]
        config["family"]["children"] = [
            {"label": c, "portalAliases": [], "calendarName": "Family"}
            for c in children
        ]
    config["family"]["calendarWriteMode"] = args.calendar_write_mode
    config["portal"].setdefault("auth", {})["mode"] = args.auth_mode
    config["portal"]["auth"]["secretRef"] = args.secret_ref
    config["digest"]["cadence"] = args.cadence
    config["digest"]["deliveryMode"] = args.delivery_mode
    config["initializedDate"] = today

    site_config = load_json(assets / "site-config.example.json")
    if args.portal_name:
        site_config["portal"] = args.portal_name
    if args.home_url:
        try:
            from urllib.parse import urlparse

            parsed = urlparse(args.home_url)
            if parsed.scheme and parsed.netloc:
                site_config["baseUrl"] = f"{parsed.scheme}://{parsed.netloc}"
        except Exception:
            pass
    site_config["lastVerified"] = None

    action_items = load_json(assets / "action-items.empty.json")

    outputs = []
    for path, data in [
        (target / "config.json", config),
        (target / "site-config.json", site_config),
        (target / "action-items.json", action_items),
    ]:
        if path.exists():
            outputs.append(f"exists: {path}")
        else:
            write_json(path, data)
            outputs.append(f"created: {path}")

    sample_summary = target / f"summary-{today}.md"
    if not sample_summary.exists():
        sample_summary.write_text(
            f"# School Portal Digest — {today}\n\n"
            "## Scan Status\n"
            "- Portal: Not checked yet\n"
            "- Surfaces checked: None\n"
            "- Blockers: First login/walkthrough not completed\n\n"
            "## 1. Action Items\nNo portal scan has run yet.\n\n"
            "## 2. Child-Specific Calendar\nNo portal scan has run yet.\n\n"
            "## 3. Worth Knowing\nNo portal scan has run yet.\n\n"
            "## 4. Check-In Guidance\nNo portal scan has run yet.\n",
            encoding="utf-8",
        )
        outputs.append(f"created: {sample_summary}")
    else:
        outputs.append(f"exists: {sample_summary}")

    print("School Portal Digest local setup")
    print(f"Today: {today}")
    for line in outputs:
        print(f"- {line}")
    print("\nNext steps:")
    print("1. Review/edit config.json for family labels, auth mode, schedule, and preferences.")
    print("2. Complete first login or local secret setup for the selected auth mode.")
    print("3. Run a read-only walkthrough to update site-config.json.")
    print(f"4. First real digest should write summary-{today}.md using today's date.")
    print("5. Schedule the recurring run after the school day if dinner/check-in signals matter.")
    print("\nDo not put passwords, cookies, MFA codes, or raw portal dumps in these files or chat.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
