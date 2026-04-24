from pathlib import Path

from mas.system import MultiAgentBuilder


def test_builder_generates_working_prototype(tmp_path: Path):
    summary = MultiAgentBuilder().build("Idea: internal ticket triage assistant", output_dir=tmp_path)

    assert summary.test_report.passed is True
    assert summary.iterations >= 1
    assert any(m.name == "evaluation" and m.status == "done" for m in summary.milestones)

    generated = list(tmp_path.glob("iteration_*/prototype/app/service.py"))
    assert generated, "Expected generated prototype service module"
