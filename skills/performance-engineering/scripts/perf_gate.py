#!/usr/bin/env python3
"""Compare performance metric snapshots against a budget.

Usage:
    python perf_gate.py before.json after.json --budget budget.json
    python perf_gate.py before.json after.json --budget budget.json --json

Input:
    {"metrics": {"api.orders.p95_ms": 240, "web.lcp_ms": 2100}}

Budget:
    {
      "api.orders.p95_ms": {"max": 300, "max_regression_pct": 10},
      "web.lcp_ms": {"max": 2500}
    }

Exit codes: 0 all pass, 1 budget violation, 2 invalid input.
No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_json(path: str) -> dict:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"error: file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"error: invalid JSON in {path}: {exc}")
    if not isinstance(data, dict):
        raise SystemExit(f"error: {path} must contain a JSON object")
    return data


def metrics_from(data: dict, path: str) -> dict:
    metrics = data.get("metrics", data)
    if not isinstance(metrics, dict):
        raise SystemExit(f"error: {path} metrics must be an object")
    result = {}
    for key, value in metrics.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise SystemExit(f"error: {path} metric {key!r} must be numeric")
        result[str(key)] = float(value)
    return result


def fmt(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return f"{value:.3f}".rstrip("0").rstrip(".")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail when metrics exceed a budget.")
    parser.add_argument("before", help="baseline metrics JSON")
    parser.add_argument("after", help="new metrics JSON")
    parser.add_argument("--budget", required=True, help="budget JSON")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = parser.parse_args()

    before = metrics_from(load_json(args.before), args.before)
    after = metrics_from(load_json(args.after), args.after)
    budget = load_json(args.budget)

    missing = sorted(set(before) - set(after))
    if missing:
        raise SystemExit(f"error: metrics missing from after snapshot: {', '.join(missing)}")

    rows = []
    failures = 0
    for name, rules in sorted(budget.items()):
        if not isinstance(rules, dict):
            raise SystemExit(f"error: budget for {name!r} must be an object")
        if name not in after:
            raise SystemExit(f"error: budget metric {name!r} missing from after snapshot")
        if name not in before:
            raise SystemExit(f"error: budget metric {name!r} missing from before snapshot")

        old = before[name]
        new = after[name]
        delta_pct = None if old == 0 else ((new - old) / abs(old)) * 100.0

        status = "pass"
        reasons = []
        max_value = rules.get("max")
        max_regression = rules.get("max_regression_pct")

        if max_value is not None and new > float(max_value):
            status = "fail"
            reasons.append(f"max {fmt(float(max_value))} exceeded")
        if max_regression is not None and delta_pct is not None:
            if delta_pct > float(max_regression):
                status = "fail"
                reasons.append(f"regression {delta_pct:.1f}% > {fmt(float(max_regression))}%")

        if status == "fail":
            failures += 1

        rows.append(
            {
                "metric": name,
                "before": old,
                "after": new,
                "delta_pct": None if delta_pct is None else round(delta_pct, 2),
                "status": status,
                "reasons": reasons,
            }
        )

    if args.json:
        print(json.dumps({"status": "fail" if failures else "pass", "rows": rows}, indent=2))
    else:
        width = max([len("metric")] + [len(r["metric"]) for r in rows]) if rows else 6
        print(f"{'metric'.ljust(width)}  {'before':>10}  {'after':>10}  {'delta':>8}  status")
        print(f"{'-' * width}  {'-' * 10}  {'-' * 10}  {'-' * 8}  ------")
        for row in rows:
            delta = "-" if row["delta_pct"] is None else f"{row['delta_pct']:+.1f}%"
            detail = "" if row["status"] == "pass" else "  (" + "; ".join(row["reasons"]) + ")"
            print(
                f"{row['metric'].ljust(width)}  {fmt(row['before']):>10}  "
                f"{fmt(row['after']):>10}  {delta:>8}  {row['status']}{detail}"
            )
        print()
        print("PASS" if failures == 0 else f"FAIL: {failures} budget violation(s)")

    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
