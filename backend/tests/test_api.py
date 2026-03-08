from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_project_workflow_happy_path() -> None:
    create = client.post(
        "/projects",
        json={
            "title": "test project",
            "raw_idea": "top-down action survival with escalating waves",
            "target_platform": "PC",
            "target_engine": "web",
        },
    )
    assert create.status_code == 200
    project_id = create.json()["project"]["project_id"]

    assert client.post(f"/projects/{project_id}/analyze").status_code == 200
    assert client.post(f"/projects/{project_id}/scope").status_code == 200
    assert client.post(f"/projects/{project_id}/docs").status_code == 200
    assert client.post(f"/projects/{project_id}/codegen").status_code == 200

    review = client.post(
        f"/projects/{project_id}/review",
        json={"feedback_text": "opening minute is unclear and difficulty spikes too hard"},
    )
    assert review.status_code == 200
    assert client.post(f"/projects/{project_id}/iterate").status_code == 200
