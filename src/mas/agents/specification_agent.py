from __future__ import annotations

from mas.models import ProductSpec


class SpecificationAgent:
    """Planning layer: translates a high-level idea into executable product specs."""

    def generate(self, idea: str) -> ProductSpec:
        features = [
            "Core domain service",
            "Input validation",
            "Simple persistence",
            "Reporting endpoint",
        ]
        if "auth" in idea.lower() or "secure" in idea.lower():
            features.append("Role-based access controls")

        return ProductSpec(
            idea=idea,
            requirements=[
                "Prototype should run with Python standard library only",
                "System must be modular and testable",
                "Agents must emit structured logs",
            ],
            features=features,
            user_stories=[
                "As a product manager I can describe an idea and receive a runnable prototype",
                "As an engineer I can inspect generated architecture and tradeoffs",
                "As QA I can execute repeatable tests and get failure reports",
            ],
            api_contracts=[
                "POST /items -> create domain item",
                "GET /items -> list items",
                "GET /health -> service health",
            ],
            assumptions=[
                "Single-tenant prototype environment",
                "No external SaaS dependencies required",
            ],
            constraints=[
                "Keep dependencies minimal",
                "Prefer synchronous execution for deterministic tests",
            ],
            missing_requirements=[
                "Define target traffic and latency SLOs",
                "Define compliance obligations (PII/retention)",
            ],
        )
