from __future__ import annotations

import subprocess
import os
from pathlib import Path

from mas.models import ImplementationArtifact, TestReport


class TestingAgent:
    """Verification layer: runs unit and integration tests and reports failures."""

    def validate(self, artifact: ImplementationArtifact) -> TestReport:
        env = {**os.environ, "PYTHONPATH": str(artifact.root_dir)}
        unit = subprocess.run(
            ["python", "-m", "pytest", "tests/test_service.py", "-q"],
            cwd=artifact.root_dir,
            capture_output=True,
            text=True,
            env=env,
        )
        integration = subprocess.run(
            ["python", "-m", "pytest", "tests/test_integration.py", "-q"],
            cwd=artifact.root_dir,
            capture_output=True,
            text=True,
            env=env,
        )

        failures = []
        if unit.returncode != 0:
            failures.append({"suite": "unit", "output": unit.stdout + unit.stderr})
        if integration.returncode != 0:
            failures.append({"suite": "integration", "output": integration.stdout + integration.stderr})

        return TestReport(
            passed=not failures,
            unit_results=unit.stdout + unit.stderr,
            integration_results=integration.stdout + integration.stderr,
            failures=failures,
        )
