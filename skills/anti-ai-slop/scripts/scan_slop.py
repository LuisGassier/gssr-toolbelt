#!/usr/bin/env python3
"""Heuristic scanner for AI-slop patterns in text and code.

Usage:
    python scan_slop.py [paths...] [--json] [--fail-on low|medium|high]
    python scan_slop.py README.md src/ --fail-on high

Exit codes:
    0  no findings at or above --fail-on (default: none)
    1  findings at or above the threshold
    2  invalid arguments

The scanner is deliberately conservative and heuristic. A finding is a candidate for human
review, not an automatic edit. It skips lockfiles, vendored code, build output, and binaries.
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
    ".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", ".next", ".nuxt",
    "coverage", ".venv", "venv", "env", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".turbo", ".cache", "target", "out",
}
SKIP_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "Cargo.lock",
    "poetry.lock", "Pipfile.lock", "composer.lock", "go.sum", "Gemfile.lock",
}
TEXT_EXTS = {
    ".md", ".mdx", ".txt", ".rst", ".html", ".htm", ".js", ".jsx", ".ts", ".tsx",
    ".mjs", ".cjs", ".vue", ".svelte", ".py", ".rb", ".go", ".rs", ".java", ".kt",
    ".php", ".cs", ".css", ".scss", ".sass", ".json", ".yaml", ".yml", ".toml",
    ".sh", ".bash", ".zsh", ".sql", ".graphql", ".gql",
}
CODE_EXTS = {
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".py", ".rb",
    ".go", ".rs", ".java", ".kt", ".php", ".cs",
}
SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3}

# (id, category, severity, regex, note, extensions or None)
PATTERNS = [
    (
        "hype-words", "copy", "medium",
        r"\b(seamless(?:ly)?|effortless(?:ly)?|cutting[- ]edge|revolutionary|"
        r"game[- ]changer|best[- ]in[- ]class|world[- ]class|industry[- ]leading|"
        r"supercharge|unleash|elevate|leverage|utilize)\b",
        "Hype or inflated word; state the concrete behavior or delete it.", None,
    ),
    (
        "filler-transitions", "copy", "low",
        r"\b(moreover|furthermore|additionally|in conclusion|it'?s worth noting|"
        r"generally speaking|in today'?s fast[- ]paced|let'?s dive in|delve into)\b",
        "Filler or hedge; cut to the point.", None,
    ),
    (
        "ai-voice", "copy", "medium",
        r"\b(as an ai|i hope this helps|certainly!|here'?s a breakdown|"
        r"i cannot browse|as a language model)\b",
        "Assistant voice leaked into the artifact; rewrite in the product's voice.", None,
    ),
    (
        "fake-proof", "substance", "high",
        r"\b(trusted by (?:thousands|millions|\d[\d,]*)|99\.9% uptime|10x faster|"
        r"thousands of (?:users|customers|teams)|industry[- ]leading)\b",
        "Unsupported social proof or metric; source it or remove it.", None,
    ),
    (
        "placeholder-data", "substance", "high",
        r"\b(john doe|jane doe|acme (?:corp|inc|co)|lorem ipsum)\b",
        "Placeholder presented as real data; label it or replace it.", None,
    ),
    (
        "emoji-heading", "craft", "low",
        r"^#{1,6}\s.*[\U0001F300-\U0001FAFF\u2600-\u27BF]",
        "Emoji heading; use a plain, scannable heading.", {".md", ".mdx", ".html"},
    ),
    (
        "todo-marker", "code", "medium",
        r"\b(TODO|FIXME|XXX)\b",
        "Unfinished marker; implement, remove, or link a tracked issue.", CODE_EXTS,
    ),
    (
        "console-log", "code", "medium",
        r"\bconsole\.(?:log|debug)\s*\(",
        "Debug logging in code; use structured logging or remove it.", {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte"},
    ),
    (
        "python-print", "code", "low",
        r"^\s*print\(",
        "Print statement; use structured logging or remove it.", {".py"},
    ),
    (
        "silent-catch", "code", "high",
        r"catch\s*(?:\([^)]*\))?\s*\{\s*\}|except[^:]*:\s*pass\b",
        "Swallowed error; handle, rethrow, or remove the catch.", CODE_EXTS,
    ),
    (
        "type-suppression", "code", "medium",
        r"(@ts-ignore|@ts-expect-error|#\s*type:\s*ignore|eslint-disable(?:-next-line)?)",
        "Suppressed check; fix the type/lint or isolate with a reason.", CODE_EXTS,
    ),
    (
        "commented-code", "code", "low",
        r"^\s*(?://|#)\s*(?:const|let|var|function|def|class|if|for|while|return|import|export)\b",
        "Commented-out code; delete it — version control remembers.", CODE_EXTS,
    ),
    (
        "vague-name", "code", "low",
        r"\b(?:function|def|const|let|var|class)\s+(?:handleData|processData|doWork|"
        r"handleStuff|doStuff|manageData|dataManager|utils?|helpers?)\b",
        "Vague identifier; rename to the domain concept.", CODE_EXTS,
    ),
    (
        "sleep-in-test", "test", "high",
        r"\b(?:sleep|setTimeout|time\.Sleep)\s*\(\s*\d+\s*\)",
        "Fixed sleep; await the real condition instead.", CODE_EXTS,
    ),
    (
        "vague-test-name", "test", "medium",
        r"\b(?:test1|test2|testWorks|should work|works fine|test_create|test_update)\b",
        "Vague test name; describe the behavior and condition.", CODE_EXTS,
    ),
    (
        "purple-gradient", "ui", "medium",
        r"(?:from|via|to)-(?:purple|indigo|violet|fuchsia)-\d{2,3}",
        "Default purple/indigo gradient palette; choose a direction tied to the product.",
        {".jsx", ".tsx", ".html", ".vue", ".svelte", ".css", ".scss"},
    ),
    (
        "glass-everywhere", "ui", "low",
        r"\bbackdrop-blur(?:-\w+)?\b",
        "Glassmorphism surface; use it only where depth/context justifies it.",
        {".jsx", ".tsx", ".html", ".vue", ".svelte", ".css", ".scss"},
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
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith(".git"))
            for name in sorted(files):
                if name in SKIP_FILES:
                    continue
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


def scan_file(path: Path, max_per_pattern: int) -> list[dict]:
    if path.suffix.lower() not in TEXT_EXTS:
        return []
    text = read_text(path)
    if text is None:
        return []

    findings: list[dict] = []
    counts: dict[str, int] = {}
    lines = text.splitlines()

    for pid, category, severity, pattern, note, exts in PATTERNS:
        if exts is not None and path.suffix.lower() not in exts:
            continue
        compiled = re.compile(pattern, re.IGNORECASE if pid not in {"emoji-heading"} else 0)
        for line_no, line in enumerate(lines, start=1):
            if counts.get(pid, 0) >= max_per_pattern:
                break
            match = compiled.search(line)
            if match:
                excerpt = line.strip()
                if len(excerpt) > 160:
                    excerpt = excerpt[:157] + "..."
                findings.append(
                    {
                        "file": str(path),
                        "line": line_no,
                        "pattern": pid,
                        "category": category,
                        "severity": severity,
                        "excerpt": excerpt,
                        "note": note,
                    }
                )
                counts[pid] = counts.get(pid, 0) + 1

    # File-level signal: generic module names.
    if path.name.lower() in {"utils.ts", "utils.js", "utils.py", "helpers.ts", "helpers.js",
                             "helpers.py", "common.ts", "common.js", "misc.ts", "misc.js"}:
        findings.append(
            {
                "file": str(path),
                "line": 1,
                "pattern": "generic-module",
                "category": "code",
                "severity": "medium",
                "excerpt": path.name,
                "note": "Generic module name; split by domain concept or make it local.",
            }
        )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan for AI-slop candidates.")
    parser.add_argument("paths", nargs="*", default=["."], help="files or directories")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--fail-on", choices=["none", "low", "medium", "high"], default="none",
        help="exit 1 when a finding at or above this severity exists",
    )
    parser.add_argument("--max-per-pattern", type=int, default=50, help="cap per file/pattern")
    args = parser.parse_args()
    if args.max_per_pattern < 1:
        parser.error("--max-per-pattern must be >= 1")

    paths = args.paths or ["."]
    all_findings: list[dict] = []
    for path in iter_files(paths):
        all_findings.extend(scan_file(path, args.max_per_pattern))

    all_findings.sort(key=lambda f: (f["file"], f["line"], f["pattern"]))
    summary: dict[str, int] = {}
    for finding in all_findings:
        summary[finding["severity"]] = summary.get(finding["severity"], 0) + 1

    if args.json:
        print(json.dumps(
            {"findings": all_findings, "summary": summary,
             "files_scanned": len({f["file"] for f in all_findings})},
            indent=2,
        ))
    else:
        current = None
        for finding in all_findings:
            if finding["file"] != current:
                current = finding["file"]
                print(f"\n{current}")
            print(
                f"  {finding['line']:>5}  {finding['severity']:<6}  "
                f"{finding['pattern']:<18}  {finding['excerpt']}"
            )
        print()
        if not all_findings:
            print("No slop candidates found. (Absence of findings is not proof of quality.)")
        else:
            parts = [f"{count} {sev}" for sev, count in sorted(
                summary.items(), key=lambda kv: -SEVERITY_RANK[kv[0]]
            )]
            print(f"{len(all_findings)} candidate(s): " + ", ".join(parts))
            print("Review candidates in context; the scanner is heuristic.")

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
