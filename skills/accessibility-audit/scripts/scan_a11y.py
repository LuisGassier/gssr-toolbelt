#!/usr/bin/env python3
"""Static accessibility scanner for common HTML/JSX defects.

Usage:
    python scan_a11y.py [paths...] [--json] [--fail-on low|medium|high]
    python scan_a11y.py src/ --fail-on high

This is a floor, not an audit. It cannot test focus order, keyboard traps, screen-reader
announcements, contrast, or cognitive load. Use it with the accessibility-audit workflow and
real assistive technology.

Exit codes: 0 clear at threshold, 1 findings at threshold, 2 invalid input.
No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Iterable

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", ".next", ".nuxt", "coverage",
    ".venv", "venv", "__pycache__", "target", "out",
}
EXTS = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".css", ".scss", ".sass"}
SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3}

# (id, severity, regex, note, extensions)
PATTERNS = [
    (
        "img-missing-alt", "high",
        r"<img\b(?![^>]*\balt\s*=)[^>]*>",
        "Image has no alt attribute; use meaningful alt text or alt=\"\" if decorative.",
        {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"},
    ),
    (
        "html-missing-lang", "high",
        r"<html\b(?![^>]*\blang\s*=)[^>]*>",
        "Set the page language: <html lang=\"en\">.",
        {".html", ".htm"},
    ),
    (
        "empty-button", "high",
        r"<button\b[^>]*>\s*</button>",
        "Empty button; add visible text or an aria-label that names the action.",
        {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"},
    ),
    (
        "positive-tabindex", "high",
        r"\btab(?:I|i)ndex\s*=\s*[\"'{]?\s*[1-9]\d*",
        "Positive tabindex breaks natural focus order; use 0/-1 and DOM order.",
        EXTS,
    ),
    (
        "outline-removed", "high",
        r"outline\s*:\s*(?:none|0)(?!\s*;?\s*})",
        "Focus outline removed; provide a visible :focus-visible indicator instead.",
        {".css", ".scss", ".sass", ".html", ".jsx", ".tsx", ".vue", ".svelte"},
    ),
    (
        "click-on-div", "high",
        r"<(?:div|span|li|td)\b[^>]*\bon(?:Click|click)\s*=",
        "Click handler on a non-interactive element; use <button> or add role, tabindex, and keyboard handling.",
        {".jsx", ".tsx", ".html", ".htm", ".vue", ".svelte"},
    ),
    (
        "role-button-no-tabindex", "high",
        r"<(?:div|span)\b(?=[^>]*\brole\s*=\s*[\"']button[\"'])(?![^>]*\btab(?:I|i)ndex\s*=)[^>]*>",
        "role=button without tabindex; prefer <button>, or add tabindex=0 and Enter/Space handling.",
        {".jsx", ".tsx", ".html", ".htm", ".vue", ".svelte"},
    ),
    (
        "anchor-no-href", "medium",
        r"<a\b(?![^>]*\bhref\s*=)[^>]*>",
        "Anchor without href is not focusable; use <button> or add a real href.",
        {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"},
    ),
    (
        "blank-target-no-rel", "medium",
        r"<(?:a|form)\b(?=[^>]*\btarget\s*=\s*[\"']_blank[\"'])(?![^>]*\brel\s*=\s*[\"'][^\"']*noopener)[^>]*>",
        "target=_blank without rel=noopener/noreferrer; add it to prevent window.opener access.",
        {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"},
    ),
    (
        "viewport-no-zoom", "high",
        r"<meta\b[^>]*name\s*=\s*[\"']viewport[\"'][^>]*content\s*=\s*[\"'][^\"']*(?:user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0)?)",
        "Viewport disables zoom; users must be able to zoom to 200%.",
        {".html", ".htm"},
    ),
    (
        "iframe-no-title", "medium",
        r"<iframe\b(?![^>]*\btitle\s*=)[^>]*>",
        "Iframe has no title; add a descriptive title for screen-reader users.",
        {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"},
    ),
    (
        "aria-hidden-focusable", "medium",
        r"<[^>]*\baria-hidden\s*=\s*[\"']true[\"'][^>]*(?:\btab(?:I|i)ndex|\bon(?:Click|click))[^>]*>",
        "aria-hidden element contains focus/click behavior; hidden content must not be focusable.",
        EXTS,
    ),
    (
        "autofocus", "low",
        r"\bautoFocus\b|\bautofocus\b",
        "Autofocus can disorient keyboard/screen-reader users; use it only when the task clearly starts there.",
        {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"},
    ),
    (
        "placeholder-only-input", "medium",
        r"<input\b[^>]*\bplaceholder\s*=[^>]*>",
        "Input has a placeholder; verify it also has a persistent visible label associated with the field.",
        {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"},
    ),
    (
        "mouse-only-handler", "low",
        r"\bonMouse(?:Over|Out|Enter|Leave)\s*=",
        "Mouse-only hover handler; provide equivalent focus/keyboard behavior.",
        {".jsx", ".tsx", ".html", ".htm", ".vue", ".svelte"},
    ),
    (
        "click-here-link", "low",
        r">\s*(?:click here|here|read more|learn more)\s*<",
        "Vague link text; name the destination or action for screen-reader link lists.",
        {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"},
    ),
]


def iter_files(paths: Iterable[str]) -> Iterable[Path]:
    for raw in paths:
        path = Path(raw)
        if path.is_file():
            yield path
            continue
        if not path.exists():
            print(f"warning: path not found: {raw}", file=sys.stderr)
            continue
        for root, dirs, files in os.walk(path):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for name in sorted(files):
                yield Path(root) / name


def read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > 1_500_000:
            return None
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw[:4096]:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def excerpt_for(text: str, offset: int) -> str:
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    if line_end == -1:
        line_end = len(text)
    excerpt = text[line_start:line_end].strip()
    return excerpt if len(excerpt) <= 160 else excerpt[:157] + "..."


def scan_file(path: Path) -> list[dict]:
    if path.suffix.lower() not in EXTS:
        return []
    text = read_text(path)
    if text is None:
        return []

    findings: list[dict] = []
    for rule_id, severity, pattern, note, exts in PATTERNS:
        if path.suffix.lower() not in exts:
            continue
        compiled = re.compile(pattern, re.IGNORECASE if rule_id != "click-here-link" else 0)
        for match in compiled.finditer(text):
            findings.append(
                {
                    "file": str(path),
                    "line": line_for_offset(text, match.start()),
                    "rule": rule_id,
                    "severity": severity,
                    "excerpt": excerpt_for(text, match.start()),
                    "note": note,
                }
            )

    # Duplicate IDs break label/aria references and parsing.
    ids = re.findall(r"\bid\s*=\s*[\"']([^\"']+)[\"']", text)
    seen: dict[str, int] = {}
    for value in ids:
        seen[value] = seen.get(value, 0) + 1
    for value, count in seen.items():
        if count > 1:
            findings.append(
                {
                    "file": str(path),
                    "line": line_for_offset(text, text.find(f'id="{value}"') if f'id="{value}"' in text else 0),
                    "rule": "duplicate-id",
                    "severity": "medium",
                    "excerpt": f'id="{value}" appears {count} times',
                    "note": "Duplicate IDs break label/aria references and parsing.",
                }
            )

    # Deduplicate identical rule/line findings.
    unique: dict[tuple, dict] = {}
    for finding in findings:
        key = (finding["file"], finding["line"], finding["rule"])
        unique.setdefault(key, finding)
    return sorted(unique.values(), key=lambda f: (f["line"], f["rule"]))


def main() -> int:
    parser = argparse.ArgumentParser(description="Static accessibility scanner.")
    parser.add_argument("paths", nargs="*", default=["."], help="files or directories")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--fail-on", choices=["none", "low", "medium", "high"], default="none",
        help="exit 1 when a finding at or above this severity exists",
    )
    args = parser.parse_args()

    paths = args.paths or ["."]
    all_findings: list[dict] = []
    for path in iter_files(paths):
        all_findings.extend(scan_file(path))

    summary: dict[str, int] = {}
    for finding in all_findings:
        summary[finding["severity"]] = summary.get(finding["severity"], 0) + 1

    if args.json:
        print(json.dumps({"findings": all_findings, "summary": summary}, indent=2))
    else:
        current = None
        for finding in all_findings:
            if finding["file"] != current:
                current = finding["file"]
                print(f"\n{current}")
            print(
                f"  {finding['line']:>5}  {finding['severity']:<6}  "
                f"{finding['rule']:<26}  {finding['excerpt']}"
            )
        print()
        if not all_findings:
            print("No static a11y findings. This does not mean the UI is accessible.")
        else:
            parts = [f"{count} {sev}" for sev, count in sorted(
                summary.items(), key=lambda kv: -SEVERITY_RANK[kv[0]]
            )]
            print(f"{len(all_findings)} finding(s): " + ", ".join(parts))
            print("Verify with keyboard, screen reader, contrast, and zoom tests.")

    if args.fail_on != "none":
        threshold = SEVERITY_RANK[args.fail_on]
        if any(SEVERITY_RANK[f["severity"]] >= threshold for f in all_findings):
            return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
