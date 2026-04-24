from __future__ import annotations

from pathlib import Path

from mas.models import EvaluationReport, ImplementationArtifact, TestReport


class EvaluationAgent:
    """Evaluates quality, maintainability, scalability, and security posture."""

    def evaluate(self, artifact: ImplementationArtifact, tests: TestReport) -> EvaluationReport:
        py_files = list((artifact.root_dir / "app").glob("*.py"))
        total_lines = sum(len(p.read_text().splitlines()) for p in py_files)

        maintainability = [
            "Modules are small and have explicit responsibilities",
            "Generated tests cover core create/list behavior",
        ]
        scalability_risks = [
            "JSON file persistence will become a bottleneck under concurrent writes",
            "Single process execution limits throughput",
        ]
        security = [
            "No authentication layer in generated API contracts",
            "No rate-limiting or abuse controls",
        ]

        refactor = [
            "Introduce repository interface and swap JSON adapter for SQL backend",
            "Add async worker queue for long-running build tasks",
        ]

        arch_issues = []
        if total_lines > 400:
            arch_issues.append("Generated modules are too large; split by domain.")
        if not tests.passed:
            arch_issues.append("Unstable test suite suggests missing contract boundaries.")

        return EvaluationReport(
            code_quality_score=0.92 if tests.passed else 0.6,
            maintainability_notes=maintainability,
            scalability_risks=scalability_risks,
            security_concerns=security,
            refactor_suggestions=refactor,
            architecture_issues=arch_issues,
        )
