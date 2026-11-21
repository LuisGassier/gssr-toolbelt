#!/usr/bin/env python3
"""Validate Agent Skills in this repository.

Checks the agentskills.io frontmatter contract, repo conventions, body size, referenced
files, and eval presence. No third-party dependencies.

Usage:
    python scripts/validate-skills.py
    python scripts/validate-skills.py --strict
    python scripts/validate-skills.py --json

Exit codes: 0 valid, 1 errors (or warnings with --strict).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REF_RE = re.compile(r"(?:\(|`)((?:references|scripts|assets)/[^)`\s]+)")
MAX_BODY_LINES = 500
MAX_BODY_TOKENS = 5000
MAX_DESCRIPTION = 1024


def parse_frontmatter(text: str) -> tuple[dict, str, str | None]:
    if not text.startswith("---"):
        return {}, text, "missing YAML frontmatter"
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text, "unterminated YAML frontmatter"
    raw = parts[1]
    body = parts[2].lstrip("\n")
    data: dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith(('"', "'")) and value.endswith(('"', "'")) and len(value) >= 2:
            value = value[1:-1]
        data[key.strip()] = value
    return data, body, None


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def validate_skill(path: Path, strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    name = path.name
    skill_file = path / "SKILL.md"

    if not skill_file.is_file():
        return [f"{name}: missing SKILL.md"], warnings

    text = skill_file.read_text(encoding="utf-8")
    data, body, fm_error = parse_frontmatter(text)
    if fm_error:
        errors.append(f"{name}: {fm_error}")
        return errors, warnings

    fm_name = data.get("name", "")
    description = data.get("description", "")

    if not fm_name:
        errors.append(f"{name}: frontmatter missing 'name'")
    elif fm_name != name:
        errors.append(f"{name}: name '{fm_name}' does not match directory")
    elif not NAME_RE.match(fm_name):
        errors.append(f"{name}: name must be lowercase alphanumeric with single hyphens")
    elif len(fm_name) > 64:
        errors.append(f"{name}: name exceeds 64 characters")

    if not description:
        errors.append(f"{name}: frontmatter missing 'description'")
    else:
        if len(description) > MAX_DESCRIPTION:
            errors.append(f"{name}: description exceeds {MAX_DESCRIPTION} characters")
        if len(description) < 80:
            warnings.append(f"{name}: description is short; add trigger context")
        if "use " not in description.lower():
            warnings.append(f"{name}: description does not say when to use the skill")
        if "\n" in description:
            warnings.append(f"{name}: description spans lines; keep it a single string")

    body_lines = len(body.splitlines())
    body_tokens = estimate_tokens(body)
    if body_lines > MAX_BODY_LINES:
        warnings.append(f"{name}: body has {body_lines} lines (>{MAX_BODY_LINES})")
    if body_tokens > MAX_BODY_TOKENS:
        warnings.append(f"{name}: body ~{body_tokens} tokens (>{MAX_BODY_TOKENS})")

    for ref in sorted(set(REF_RE.findall(text))):
        target = path / ref
        if not target.exists():
            errors.append(f"{name}: referenced file does not exist: {ref}")

    evals = path / "evals" / "evals.json"
    if not evals.is_file():
        warnings.append(f"{name}: no evals/evals.json")
    else:
        try:
            payload = json.loads(evals.read_text(encoding="utf-8"))
            if not isinstance(payload.get("evals"), list) or not payload["evals"]:
                warnings.append(f"{name}: evals.json has no evals")
        except json.JSONDecodeError as exc:
            errors.append(f"{name}: invalid evals.json: {exc}")

    if "metadata" not in data:
        warnings.append(f"{name}: no metadata block (author/version recommended)")

    if strict:
        errors.extend(warnings)
        warnings = []
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate skills in this repository.")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    if not SKILLS_DIR.is_dir():
        print(f"error: skills directory not found at {SKILLS_DIR}", file=sys.stderr)
        return 1

    results = []
    all_errors: list[str] = []
    all_warnings: list[str] = []
    names: dict[str, str] = {}

    for path in sorted(SKILLS_DIR.iterdir()):
        if not path.is_dir():
            continue
        if path.name.endswith("-workspace") or path.name.startswith("."):
            continue
        errors, warnings = validate_skill(path, args.strict)
        results.append({"skill": path.name, "errors": errors, "warnings": warnings})
        all_errors.extend(errors)
        all_warnings.extend(warnings)
        if path.name in names:
            all_errors.append(f"{path.name}: duplicate skill directory")
        names[path.name] = str(path)

    if args.json:
        print(json.dumps(
            {"results": results, "errors": len(all_errors), "warnings": len(all_warnings)},
            indent=2,
        ))
    else:
        for result in results:
            status = "FAIL" if result["errors"] else ("WARN" if result["warnings"] else "OK")
            print(f"[{status}] {result['skill']}")
            for error in result["errors"]:
                print(f"  error: {error}")
            for warning in result["warnings"]:
                print(f"  warn:  {warning}")
        print()
        print(f"{len(results)} skills, {len(all_errors)} error(s), {len(all_warnings)} warning(s)")

    return 1 if all_errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
