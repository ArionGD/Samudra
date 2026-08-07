"""End-to-end smoke test for the session lifecycle: create → respond →
complete → monitor → withdraw (real delete).
"""

from fastapi.testclient import TestClient


def _create_session(client: TestClient) -> dict:
    resp = client.post(
        "/session",
        json={
            "recruitment_channel": "dev_community",
            "consent_version": "v1",
            "consent_research": True,
            "consent_open_data": False,
            "device_type": "desktop",
            "input_method": "mouse_keyboard",
            "viewport_width": 1440,
        },
    )
    assert resp.status_code == 201
    return resp.json()


def test_health(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_session_requires_research_consent(client: TestClient) -> None:
    resp = client.post(
        "/session",
        json={
            "recruitment_channel": "dev_community",
            "consent_version": "v1",
            "consent_research": False,
        },
    )
    assert resp.status_code == 422


def test_full_session_lifecycle(client: TestClient) -> None:
    session = _create_session(client)
    assert session["condition"] in {
        "honest_untimed",
        "honest_timed",
        "fake_timed",
        "fake_untimed",
    }

    ingest = client.post(
        f"/session/{session['session_id']}/responses",
        json={
            "responses": [
                {
                    "module_code": "M1",
                    "item_id": "blk_003",
                    "item_bank_version": "v1.0.0",
                    "position_in_module": 1,
                    "response_payload": {"most": "stmt_047", "least": "stmt_112"},
                    "latency_ms": 4231,
                }
            ]
        },
    )
    assert ingest.status_code == 204

    complete = client.post(f"/session/{session['session_id']}/complete", json={})
    assert complete.status_code == 204

    monitor = client.get("/admin/monitor", headers={"x-admin-key": "change-me-in-.env"})
    assert monitor.status_code == 200
    assert monitor.json()["total_sessions"] == 1
    assert monitor.json()["completed_sessions"] == 1


def test_admin_monitor_requires_key(client: TestClient) -> None:
    resp = client.get("/admin/monitor")
    assert resp.status_code == 401


def test_withdraw_deletes_everything(client: TestClient) -> None:
    session = _create_session(client)
    client.post(
        f"/session/{session['session_id']}/responses",
        json={
            "responses": [
                {
                    "module_code": "M1",
                    "item_id": "blk_003",
                    "item_bank_version": "v1.0.0",
                    "position_in_module": 1,
                    "response_payload": {"most": "stmt_047", "least": "stmt_112"},
                }
            ]
        },
    )

    withdraw = client.post(
        "/withdraw", json={"participant_code": session["participant_code"]}
    )
    assert withdraw.status_code == 204

    monitor = client.get("/admin/monitor", headers={"x-admin-key": "change-me-in-.env"})
    assert monitor.json()["total_sessions"] == 0


def test_withdraw_unknown_participant_404s(client: TestClient) -> None:
    resp = client.post("/withdraw", json={"participant_code": "does-not-exist"})
    assert resp.status_code == 404
