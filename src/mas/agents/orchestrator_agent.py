from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter

from mas.models import LogEvent, Milestone


@dataclass
class OrchestratorAgent:
    """Coordinates stage execution and tracks status/retries.

    Tradeoff: this orchestrator favors deterministic control flow over dynamic
    task-graph scheduling so the prototype remains easy to reason about and test.
    """

    max_retries: int = 2
    logs: list[LogEvent] = field(default_factory=list)

    def make_milestones(self) -> list[Milestone]:
        return [
            Milestone("planning"),
            Milestone("architecture"),
            Milestone("implementation"),
            Milestone("testing"),
            Milestone("evaluation"),
        ]

    def log(self, stage: str, message: str, *, level: str = "INFO", **metadata: object) -> None:
        self.logs.append(LogEvent(stage=stage, message=message, level=level, metadata=dict(metadata)))

    def run_stage(self, milestone: Milestone, fn):
        start = perf_counter()
        milestone.status = "running"
        try:
            result = fn()
            milestone.status = "done"
            self.log(milestone.name, "stage completed", duration_ms=round((perf_counter() - start) * 1000, 2))
            return result
        except Exception as exc:  # noqa: BLE001 - prototype orchestrator catches stage errors intentionally.
            milestone.retries += 1
            milestone.status = "failed"
            self.log(
                milestone.name,
                "stage failed",
                level="ERROR",
                retries=milestone.retries,
                error=str(exc),
                duration_ms=round((perf_counter() - start) * 1000, 2),
            )
            raise
