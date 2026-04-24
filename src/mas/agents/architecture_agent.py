from __future__ import annotations

from mas.models import ArchitecturePlan, ProductSpec


class ArchitectureAgent:
    """Proposes architecture boundaries and justifies tradeoffs."""

    def design(self, spec: ProductSpec) -> ArchitecturePlan:
        return ArchitecturePlan(
            overview=(
                "Layered monolith with strict module boundaries (planning, orchestration, "
                "implementation, testing, evaluation) to optimize developer velocity while "
                "remaining easy to split into services later."
            ),
            folder_structure={
                "prototype/app": "Business logic and storage adapter",
                "prototype/tests": "Unit and integration tests",
                "build_outputs": "Generated docs and summaries",
            },
            service_boundaries=[
                "Planner service boundary: transforms idea into machine-readable spec",
                "Builder service boundary: creates runnable implementation artifacts",
                "Verifier service boundary: runs tests and emits structured failures",
            ],
            database_schema={
                "items": ["id TEXT PRIMARY KEY", "title TEXT", "created_at TEXT"],
            },
            tradeoffs=[
                "File-based JSON persistence is slower than DBs but portable for prototypes",
                "Synchronous pipeline reduces throughput but simplifies retries and auditing",
            ],
        )
