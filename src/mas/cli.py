from __future__ import annotations

import argparse
import json
from pathlib import Path

from mas.system import MultiAgentBuilder


def main() -> None:
    parser = argparse.ArgumentParser(description="Build prototype via multi-agent pipeline")
    parser.add_argument("idea", help="High-level product idea")
    parser.add_argument("--output", default="build_outputs", help="Output directory")
    args = parser.parse_args()

    builder = MultiAgentBuilder()
    summary = builder.build(args.idea, output_dir=Path(args.output))

    printable = {
        "idea": summary.idea,
        "iterations": summary.iterations,
        "milestones": [{"name": m.name, "status": m.status, "retries": m.retries} for m in summary.milestones],
        "tests_passed": summary.test_report.passed,
        "risk_assessment": {
            "scalability": summary.evaluation_report.scalability_risks,
            "security": summary.evaluation_report.security_concerns,
        },
        "technical_debt": summary.technical_debt,
        "roadmap": summary.roadmap,
    }
    print(json.dumps(printable, indent=2))


if __name__ == "__main__":
    main()
