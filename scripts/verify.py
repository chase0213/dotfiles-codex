#!/usr/bin/env python3
"""Validate the tracked Codex configuration without third-party packages."""

from pathlib import Path
import re
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
VALID_SANDBOX_MODES = {"read-only", "workspace-write", "danger-full-access"}
WRITE_AGENTS = {"implementer", "test-writer"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_non_empty_string(data: dict, key: str, path: Path) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f"{path.relative_to(ROOT)}: missing non-empty {key}")
    return value.strip()


with (ROOT / "config.example.toml").open("rb") as stream:
    config = tomllib.load(stream)

agents_config = config.get("agents")
if not isinstance(agents_config, dict):
    fail("config.example.toml: missing [agents] table")
for key in ("max_threads", "max_depth"):
    value = agents_config.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        fail(f"config.example.toml: agents.{key} must be a positive integer")

agent_names: set[str] = set()
agent_paths = sorted((ROOT / "agents").glob("*.toml"))
if not agent_paths:
    fail("agents/: no custom agents found")

for path in agent_paths:
    with path.open("rb") as stream:
        data = tomllib.load(stream)
    name = require_non_empty_string(data, "name", path)
    require_non_empty_string(data, "description", path)
    require_non_empty_string(data, "developer_instructions", path)
    if name != path.stem:
        fail(f"{path.relative_to(ROOT)}: name must match filename stem")
    if name in agent_names:
        fail(f"{path.relative_to(ROOT)}: duplicate agent name {name!r}")
    agent_names.add(name)

    sandbox_mode = data.get("sandbox_mode")
    if sandbox_mode not in VALID_SANDBOX_MODES:
        fail(f"{path.relative_to(ROOT)}: invalid or missing sandbox_mode")
    expected_mode = "workspace-write" if name in WRITE_AGENTS else "read-only"
    if sandbox_mode != expected_mode:
        fail(f"{path.relative_to(ROOT)}: expected sandbox_mode={expected_mode!r}")

skill_names: set[str] = set()
skill_paths = sorted((ROOT / "skills").glob("*/SKILL.md"))
if not skill_paths:
    fail("skills/: no skills found")

for path in skill_paths:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, flags=re.DOTALL)
    if not match:
        fail(f"{path.relative_to(ROOT)}: invalid skill frontmatter delimiters")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not name or not description:
        fail(f"{path.relative_to(ROOT)}: name and description are required")
    if name != path.parent.name:
        fail(f"{path.relative_to(ROOT)}: name must match skill directory")
    if name in skill_names:
        fail(f"{path.relative_to(ROOT)}: duplicate skill name {name!r}")
    skill_names.add(name)

print(
    "Codex configuration is structurally valid "
    f"({len(agent_names)} agents, {len(skill_names)} skills)."
)
