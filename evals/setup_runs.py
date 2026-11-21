#!/usr/bin/env python3
"""Create isolated per-skill run directories from the shared fixture.

Usage:
    python evals/setup_runs.py [skill ...]

Each run gets:
    evals/runs/<skill>/repo/      writable copy of evals/fixtures/legacy-app
    evals/runs/<skill>/outputs/   for report.md and artifacts

pr-craft also gets a git repo with a baseline commit and a deliberately mixed working tree.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "evals" / "fixtures" / "legacy-app"
RUNS = ROOT / "evals" / "runs"


def run(cwd: Path, *args: str) -> None:
    subprocess.run(args, cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def prepare_messy_repo(repo: Path) -> None:
    run(repo, "git", "init", "-q")
    run(repo, "git", "config", "user.email", "eval@example.com")
    run(repo, "git", "config", "user.name", "Eval Harness")
    run(repo, "git", "add", "-A")
    run(repo, "git", "commit", "-q", "-m", "chore: baseline legacy app")

    # Feature code mixed with debug output.
    (repo / "src" / "lib" / "recommendations.js").write_text(
        "// New feature: recommendations. Still experimental.\n"
        "function recommendForUser(user) {\n"
        "  console.log('recommend', user.email);\n"
        "  return [{ id: 1, score: 0.9 }];\n"
        "}\n"
        "module.exports = { recommendForUser };\n",
        encoding="utf-8",
    )

    server = repo / "server.js"
    server.write_text(
        server.read_text(encoding="utf-8")
        + "\n// Added for the recommendations feature.\n"
        + "app.get('/api/recommendations', async (req, res) => {\n"
        + "  try {\n"
        + "    const users = await pool.query('SELECT * FROM users');\n"
        + "    res.json({ success: true, data: users.rows.map((u) => u.email) });\n"
        + "  } catch (err) {\n"
        + "    console.log(err);\n"
        + "  }\n"
        + "});\n",
        encoding="utf-8",
    )

    # Formatting-only churn.
    utils = repo / "src" / "lib" / "utils.js"
    utils.write_text(
        utils.read_text(encoding="utf-8").replace("\nfunction ", "\n\nfunction ").replace(
            '"', "'"
        ),
        encoding="utf-8",
    )

    # Unrelated docs edit.
    readme = repo / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "\n<!-- TODO: add screenshots -->\n", encoding="utf-8")


def main() -> None:
    skills = sys.argv[1:]
    if not skills:
        skills = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
        skills = [s for s in skills if not s.endswith("-workspace")]

    for skill in skills:
        run_dir = RUNS / skill
        if run_dir.exists():
            shutil.rmtree(run_dir)
        repo = run_dir / "repo"
        fixture = ROOT / "evals" / "fixtures" / "ui-reference" if skill == "image-to-ui" else FIXTURE
        shutil.copytree(fixture, repo)
        (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
        if skill == "pr-craft":
            prepare_messy_repo(repo)
        print(f"prepared {run_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
