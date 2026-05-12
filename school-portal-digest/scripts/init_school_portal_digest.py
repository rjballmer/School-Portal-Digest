#!/usr/bin/env python3
"""Initialize and validate local state for the school-portal-digest skill.

Creates a private local folder with config/state templates. This script does
not collect credentials, log into portals, or write real family data.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

VERSION = "0.2.0"

REQUIRED_FILES = ("config.json", "site-config.json", "action-items.json")
VALID_AUTH_MODES = {"browser-session", "official-oauth", "keychain", "env-token", "manual-refresh"}
VALID_CALENDAR_WRITE_MODES = {"recommend-only", "write-with-confirmation", "write-auto"}
VALID_DELIVERY_MODES = {"announce", "file-only", "none"}
VALID_CADENCES = {"on-demand", "post-school-day", "daily", "weekday-morning", "weekly"}
VALID_ACTION_STATUSES = {"open", "completed", "needs-review", "dismissed"}
VALID_CONFIDENCE = {"high", "medium", "low"}


class ValidationError(Exception):
    """Raised when local state does not match the expected structure."""


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def copy_if_missing(src: Path, dst: Path) -> str:
    if dst.exists():
        return f"exists: {dst}"
    shutil.copyfile(src, dst)
    return f"created: {dst}"


def parse_url(value: str, field_name: str) -> tuple[str, str, str | None]:
    """Return scheme/netloc plus an optional non-HTTPS warning."""
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise argparse.ArgumentTypeError(
            f"{field_name} must be an absolute http(s) URL, got: {value!r}"
        )
    warning = None
    if parsed.scheme != "https":
        warning = f"warning: {field_name} is not HTTPS: {value}"
    return parsed.scheme, parsed.netloc, warning


def validate_string(value: Any, path: str, errors: list[str], *, allow_empty: bool = False) -> None:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        errors.append(f"{path} must be a non-empty string")


def validate_url(value: Any, path: str, errors: list[str], warnings: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{path} must be a URL string")
        return
    try:
        _, _, warning = parse_url(value, path)
        if warning:
            warnings.append(warning)
    except argparse.ArgumentTypeError as exc:
        errors.append(str(exc))


def validate_config(config: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    portal = config.get("portal")
    family = config.get("family")
    digest = config.get("digest")
    privacy = config.get("privacy")
    if not isinstance(portal, dict):
        errors.append("portal must be an object")
        portal = {}
    if not isinstance(family, dict):
        errors.append("family must be an object")
        family = {}
    if not isinstance(digest, dict):
        errors.append("digest must be an object")
        digest = {}
    if not isinstance(privacy, dict):
        errors.append("privacy must be an object")
        privacy = {}

    validate_string(portal.get("name"), "portal.name", errors)
    validate_url(portal.get("loginUrl"), "portal.loginUrl", errors, warnings)
    validate_url(portal.get("homeUrl"), "portal.homeUrl", errors, warnings)

    auth = portal.get("auth")
    if not isinstance(auth, dict):
        errors.append("portal.auth must be an object")
    else:
        mode = auth.get("mode")
        if mode not in VALID_AUTH_MODES:
            errors.append(f"portal.auth.mode must be one of {sorted(VALID_AUTH_MODES)}")
        secret_ref = auth.get("secretRef")
        if secret_ref is not None and not isinstance(secret_ref, str):
            errors.append("portal.auth.secretRef must be null or a local reference string")

    children = family.get("children")
    if not isinstance(children, list) or not children:
        errors.append("family.children must contain at least one child label")
    else:
        for index, child in enumerate(children):
            child_path = f"family.children[{index}]"
            if not isinstance(child, dict):
                errors.append(f"{child_path} must be an object")
                continue
            validate_string(child.get("label"), f"{child_path}.label", errors)
            aliases = child.get("portalAliases")
            if not isinstance(aliases, list) or not all(isinstance(item, str) for item in aliases):
                errors.append(f"{child_path}.portalAliases must be a list of strings")
            validate_string(child.get("calendarName"), f"{child_path}.calendarName", errors)

    if family.get("calendarWriteMode") not in VALID_CALENDAR_WRITE_MODES:
        errors.append(f"family.calendarWriteMode must be one of {sorted(VALID_CALENDAR_WRITE_MODES)}")

    if digest.get("cadence") not in VALID_CADENCES:
        errors.append(f"digest.cadence must be one of {sorted(VALID_CADENCES)}")
    if digest.get("deliveryMode") not in VALID_DELIVERY_MODES:
        errors.append(f"digest.deliveryMode must be one of {sorted(VALID_DELIVERY_MODES)}")
    max_retention = digest.get("maxRetentionDays")
    if not isinstance(max_retention, int) or max_retention < 1:
        errors.append("digest.maxRetentionDays must be a positive integer")

    for key in ("redactNamesInSharedOutputs", "storeRawPortalText", "avoidScreenshots"):
        if not isinstance(privacy.get(key), bool):
            errors.append(f"privacy.{key} must be true or false")

    return errors, warnings


def validate_site_config(site_config: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    validate_string(site_config.get("portal"), "site-config.portal", errors)
    validate_url(site_config.get("baseUrl"), "site-config.baseUrl", errors, warnings)
    surfaces = site_config.get("surfaces")
    if not isinstance(surfaces, dict) or not surfaces:
        errors.append("site-config.surfaces must be a non-empty object")
    else:
        priorities: set[int] = set()
        for name, surface in surfaces.items():
            path = f"site-config.surfaces.{name}"
            if not isinstance(surface, dict):
                errors.append(f"{path} must be an object")
                continue
            validate_string(surface.get("label"), f"{path}.label", errors)
            validate_string(surface.get("url"), f"{path}.url", errors)
            if not isinstance(surface.get("enabled"), bool):
                errors.append(f"{path}.enabled must be true or false")
            priority = surface.get("priority")
            if not isinstance(priority, int) or priority < 1:
                errors.append(f"{path}.priority must be a positive integer")
            elif priority in priorities:
                warnings.append(f"warning: duplicate surface priority {priority} at {path}")
            priorities.add(priority)
    if not isinstance(site_config.get("selectors"), dict):
        errors.append("site-config.selectors must be an object")
    return errors, warnings


def validate_action_items(action_items: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    items = action_items.get("items")
    if not isinstance(items, list):
        errors.append("action-items.items must be a list")
        return errors, warnings
    seen_ids: set[str] = set()
    for index, item in enumerate(items):
        path = f"action-items.items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path} must be an object")
            continue
        validate_string(item.get("id"), f"{path}.id", errors)
        if item.get("id") in seen_ids:
            warnings.append(f"warning: duplicate action item id: {item.get('id')}")
        seen_ids.add(item.get("id"))
        validate_string(item.get("title"), f"{path}.title", errors)
        if item.get("status") not in VALID_ACTION_STATUSES:
            errors.append(f"{path}.status must be one of {sorted(VALID_ACTION_STATUSES)}")
        if item.get("confidence") not in VALID_CONFIDENCE:
            errors.append(f"{path}.confidence must be one of {sorted(VALID_CONFIDENCE)}")
    return errors, warnings


def validate_target(target: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not target.exists():
        return [f"target does not exist: {target}"], warnings
    if not target.is_dir():
        return [f"target is not a directory: {target}"], warnings

    for filename in REQUIRED_FILES:
        if not (target / filename).exists():
            errors.append(f"missing required file: {target / filename}")

    if errors:
        return errors, warnings

    try:
        config = load_json(target / "config.json")
        site_config = load_json(target / "site-config.json")
        action_items = load_json(target / "action-items.json")
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"], warnings

    for validator, data in [
        (validate_config, config),
        (validate_site_config, site_config),
        (validate_action_items, action_items),
    ]:
        next_errors, next_warnings = validator(data)
        errors.extend(next_errors)
        warnings.extend(next_warnings)

    if not (target / "calendar").exists():
        warnings.append(f"warning: optional calendar folder is missing: {target / 'calendar'}")

    return errors, warnings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create or validate local config/state files for School Portal Digest."
    )
    parser.add_argument("--version", action="version", version=f"School Portal Digest initializer {VERSION}")
    parser.add_argument(
        "--target",
        default="school-portal",
        help="Local state directory to create or validate. Default: school-portal",
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
        choices=sorted(VALID_CADENCES),
        default="post-school-day",
    )
    parser.add_argument(
        "--auth-mode",
        choices=sorted(VALID_AUTH_MODES),
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
        choices=sorted(VALID_DELIVERY_MODES),
        default="announce",
    )
    parser.add_argument(
        "--calendar-write-mode",
        choices=sorted(VALID_CALENDAR_WRITE_MODES),
        default="recommend-only",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate an existing target folder without creating or changing files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without writing files.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print only warnings/errors and created/existing file lines.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()

    if args.validate:
        errors, warnings = validate_target(target)
        for warning in warnings:
            print(warning)
        if errors:
            print("School Portal Digest validation failed")
            for error in errors:
                print(f"- {error}")
            return 1
        print(f"School Portal Digest validation passed: {target}")
        return 0

    url_warnings: list[str] = []
    if args.login_url:
        try:
            _, _, warning = parse_url(args.login_url, "--login-url")
        except argparse.ArgumentTypeError as exc:
            parser.error(str(exc))
        if warning:
            url_warnings.append(warning)
    if args.home_url:
        try:
            _, _, warning = parse_url(args.home_url, "--home-url")
        except argparse.ArgumentTypeError as exc:
            parser.error(str(exc))
        if warning:
            url_warnings.append(warning)

    children = None
    if args.children is not None:
        children = [c.strip() for c in args.children.split(",") if c.strip()]
        if not children:
            parser.error("--children must include at least one non-empty label when provided")

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    assets = skill_dir / "assets"
    today = datetime.now().astimezone().strftime("%Y-%m-%d")

    outputs: list[str] = []
    if not args.dry_run:
        target.mkdir(parents=True, exist_ok=True)
        (target / "calendar").mkdir(exist_ok=True)
    else:
        outputs.append(f"would create directory: {target}")
        outputs.append(f"would create directory: {target / 'calendar'}")

    config = load_json(assets / "config.example.json")
    if args.portal_name:
        config["portal"]["name"] = args.portal_name
    if args.login_url:
        config["portal"]["loginUrl"] = args.login_url
    if args.home_url:
        config["portal"]["homeUrl"] = args.home_url
    if children:
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
        parsed = urlparse(args.home_url)
        site_config["baseUrl"] = f"{parsed.scheme}://{parsed.netloc}"
    site_config["lastVerified"] = None

    action_items = load_json(assets / "action-items.empty.json")

    for path, data in [
        (target / "config.json", config),
        (target / "site-config.json", site_config),
        (target / "action-items.json", action_items),
    ]:
        if path.exists():
            outputs.append(f"exists: {path}")
        elif args.dry_run:
            outputs.append(f"would create: {path}")
        else:
            write_json(path, data)
            outputs.append(f"created: {path}")

    sample_summary = target / f"summary-{today}.md"
    if sample_summary.exists():
        outputs.append(f"exists: {sample_summary}")
    elif args.dry_run:
        outputs.append(f"would create: {sample_summary}")
    else:
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

    for warning in url_warnings:
        print(warning)

    if not args.quiet:
        print("School Portal Digest local setup")
        print(f"Version: {VERSION}")
        print(f"Today: {today}")
    for line in outputs:
        print(f"- {line}")
    if not args.quiet:
        print("\nNext steps:")
        print("1. Review/edit config.json for family labels, auth mode, schedule, and preferences.")
        print("2. Complete first login or local secret setup for the selected auth mode.")
        print("3. Run a read-only walkthrough to update site-config.json.")
        print(f"4. First real digest should write summary-{today}.md using today's date.")
        print("5. Schedule the recurring run after the school day if dinner/check-in signals matter.")
        print("6. Run this script with --validate --target <folder> to check local state later.")
        print("\nDo not put passwords, cookies, MFA codes, or raw portal dumps in these files or chat.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
