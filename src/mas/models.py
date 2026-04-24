from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class LogEvent:
    stage: str
    message: str
    level: str = "INFO"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Milestone:
    name: str
    status: str = "pending"
    retries: int = 0


@dataclass
class ProductSpec:
    idea: str
    requirements: list[str]
    features: list[str]
    user_stories: list[str]
    api_contracts: list[str]
    assumptions: list[str]
    constraints: list[str]
    missing_requirements: list[str]


@dataclass
class ArchitecturePlan:
    overview: str
    folder_structure: dict[str, str]
    service_boundaries: list[str]
    database_schema: dict[str, list[str]]
    tradeoffs: list[str]


@dataclass
class ImplementationArtifact:
    root_dir: Path
    files: dict[str, str]


@dataclass
class TestReport:
    passed: bool
    unit_results: str
    integration_results: str
    failures: list[dict[str, str]]


@dataclass
class EvaluationReport:
    code_quality_score: float
    maintainability_notes: list[str]
    scalability_risks: list[str]
    security_concerns: list[str]
    refactor_suggestions: list[str]
    architecture_issues: list[str]


@dataclass
class BuildSummary:
    idea: str
    milestones: list[Milestone]
    iterations: int
    test_report: TestReport
    evaluation_report: EvaluationReport
    logs: list[LogEvent]
    technical_debt: list[str]
    roadmap: list[str]
