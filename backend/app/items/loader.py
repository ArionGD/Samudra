"""Loads versioned item banks from the git-tracked `items/` directory.

Item banks are YAML, not database rows, so item content is reviewable in pull
requests and diffable. Loaded once into memory at startup. See
docs/04-data-schema.md and docs/10-tech-stack-and-system-design.md §"Item bank
loading".
"""

from functools import lru_cache
from pathlib import Path

import yaml

from app.config import settings

MAX_DESIRABILITY_SPREAD = 0.5


class ItemBankError(ValueError):
    pass


def _module_dir(module_code: str, version: str) -> Path:
    return Path(settings.items_dir) / module_code / version


@lru_cache
def load_statements(module_code: str, version: str) -> dict[str, dict]:
    path = _module_dir(module_code, version) / "statements.yaml"
    if not path.exists():
        raise ItemBankError(f"No statements.yaml for {module_code}/{version} at {path}")
    with path.open(encoding="utf-8") as f:
        statements = yaml.safe_load(f) or []
    return {s["id"]: s for s in statements}


@lru_cache
def load_blocks(module_code: str, version: str) -> list[dict]:
    path = _module_dir(module_code, version) / "blocks.yaml"
    if not path.exists():
        raise ItemBankError(f"No blocks.yaml for {module_code}/{version} at {path}")
    with path.open(encoding="utf-8") as f:
        blocks = yaml.safe_load(f) or []
    return blocks


def validate_desirability_spread(module_code: str, version: str) -> list[str]:
    """Returns a list of block_ids that violate the desirability-spread rule.

    This is the check that must run in CI and fail the build if non-empty —
    see docs/04-data-schema.md: "Compute desirability_spread automatically and
    fail the build if any block exceeds threshold."
    """
    statements = load_statements(module_code, version)
    violations = []
    for block in load_blocks(module_code, version):
        means = [statements[sid]["desirability_mean"] for sid in block["statements"]]
        spread = max(means) - min(means)
        if spread > MAX_DESIRABILITY_SPREAD:
            violations.append(block["block_id"])
    return violations
