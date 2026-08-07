"""Test fixtures: an isolated SQLite DB per test.

Uses a temp file rather than :memory: because the app creates two separate
engines (research/contact) and an in-memory SQLite DB is per-connection —
different engines would see different empty databases. A temp file is shared
correctly across the connections a single engine opens.

`app.config.settings` is a module-level singleton evaluated at first import,
so each test reloads `app.config`, `app.database`, and `app.main` after
pointing the env vars at a fresh temp directory — otherwise every test after
the first would silently share the first test's database.
"""

import importlib
import os
import sys
import tempfile
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["RESEARCH_DATABASE_URL"] = f"sqlite:///{os.path.join(tmp, 'research.db')}"
        os.environ["CONTACT_DATABASE_URL"] = f"sqlite:///{os.path.join(tmp, 'contact.db')}"

        for mod in list(sys.modules):
            if mod == "app" or mod.startswith("app."):
                sys.modules.pop(mod, None)

        app_main = importlib.import_module("app.main")

        with TestClient(app_main.app) as test_client:
            yield test_client

        os.environ.pop("RESEARCH_DATABASE_URL", None)
        os.environ.pop("CONTACT_DATABASE_URL", None)
