from __future__ import annotations

import json
from pathlib import Path

from mas.models import ArchitecturePlan, ImplementationArtifact, ProductSpec


class ImplementationAgent:
    """Execution layer: materializes a runnable prototype aligned to architecture."""

    def generate(self, spec: ProductSpec, architecture: ArchitecturePlan, output_dir: Path) -> ImplementationArtifact:
        root = output_dir / "prototype"
        app_dir = root / "app"
        tests_dir = root / "tests"
        app_dir.mkdir(parents=True, exist_ok=True)
        tests_dir.mkdir(parents=True, exist_ok=True)

        files: dict[str, str] = {
            "README.md": self._readme(spec, architecture),
            "app/__init__.py": "",
            "app/service.py": self._service_module(),
            "app/main.py": self._main_module(),
            "tests/test_service.py": self._unit_tests(),
            "tests/test_integration.py": self._integration_tests(),
            "data.json": json.dumps({"items": []}, indent=2),
        }

        for rel, content in files.items():
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)

        return ImplementationArtifact(root_dir=root, files=files)

    def _readme(self, spec: ProductSpec, architecture: ArchitecturePlan) -> str:
        return (
            f"# Generated Prototype\n\n"
            f"Idea: {spec.idea}\n\n"
            "## Architecture\n"
            f"{architecture.overview}\n\n"
            "## Features\n"
            + "\n".join(f"- {f}" for f in spec.features)
            + "\n"
        )

    def _service_module(self) -> str:
        return '''"""Core business service.

Tradeoff: keeps persistence as a JSON file for portability in generated prototypes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


@dataclass
class Item:
    id: str
    title: str
    created_at: str


class ItemService:
    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file
        if not self.data_file.exists():
            self.data_file.write_text(json.dumps({"items": []}))

    def _load(self) -> dict:
        return json.loads(self.data_file.read_text())

    def _save(self, payload: dict) -> None:
        self.data_file.write_text(json.dumps(payload, indent=2))

    def create_item(self, title: str) -> Item:
        if not title.strip():
            raise ValueError("title must not be empty")
        payload = self._load()
        item = Item(id=str(uuid4()), title=title.strip(), created_at=datetime.now(timezone.utc).isoformat())
        payload["items"].append(item.__dict__)
        self._save(payload)
        return item

    def list_items(self) -> list[Item]:
        payload = self._load()
        return [Item(**raw) for raw in payload["items"]]
'''

    def _main_module(self) -> str:
        return '''from __future__ import annotations

from pathlib import Path

from app.service import ItemService


def run_demo() -> None:
    service = ItemService(Path(__file__).resolve().parent.parent / "data.json")
    service.create_item("initial item")
    print(f"items={len(service.list_items())}")


if __name__ == "__main__":
    run_demo()
'''

    def _unit_tests(self) -> str:
        return '''from pathlib import Path

from app.service import ItemService


def test_create_item(tmp_path: Path):
    service = ItemService(tmp_path / "data.json")
    item = service.create_item("hello")
    assert item.title == "hello"
    assert len(service.list_items()) == 1


def test_create_item_rejects_empty_title(tmp_path: Path):
    service = ItemService(tmp_path / "data.json")
    try:
        service.create_item("   ")
    except ValueError as exc:
        assert "must not be empty" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
'''

    def _integration_tests(self) -> str:
        return '''from pathlib import Path

from app.service import ItemService


def test_end_to_end_creation_flow(tmp_path: Path):
    data_file = tmp_path / "data.json"
    service = ItemService(data_file)
    service.create_item("a")
    service.create_item("b")

    titles = [item.title for item in service.list_items()]
    assert titles == ["a", "b"]
'''
