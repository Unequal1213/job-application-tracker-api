from typing import Any

from fastapi.testclient import TestClient


def create_company(client: TestClient, name: str = "Acme") -> dict[str, Any]:
    response = client.post(
        "/companies",
        json={"name": name, "website": "https://example.com", "notes": None},
    )

    assert response.status_code == 201
    return response.json()


def create_application(
    client: TestClient,
    company_id: int,
    position_title: str = "Backend Developer",
    status: str = "saved",
) -> dict[str, Any]:
    response = client.post(
        "/applications",
        json={
            "company_id": company_id,
            "position_title": position_title,
            "job_url": "https://example.com/jobs/backend",
            "status": status,
            "source": "LinkedIn",
            "notes": "Looks interesting.",
        },
    )

    assert response.status_code == 201
    return response.json()


def test_create_application(client: TestClient) -> None:
    company = create_company(client)

    data = create_application(client, company["id"])

    assert data["id"] == 1
    assert data["company_id"] == company["id"]
    assert data["position_title"] == "Backend Developer"
    assert data["status"] == "saved"
    assert data["source"] == "LinkedIn"


def test_create_application_with_missing_company_returns_404(
    client: TestClient,
) -> None:
    response = client.post(
        "/applications",
        json={"company_id": 999, "position_title": "Backend Developer"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Company not found"}


def test_list_applications(client: TestClient) -> None:
    company = create_company(client)
    create_application(client, company["id"], position_title="Backend Developer")
    create_application(client, company["id"], position_title="API Developer")

    response = client.get("/applications")

    assert response.status_code == 200
    assert [item["position_title"] for item in response.json()] == [
        "Backend Developer",
        "API Developer",
    ]


def test_get_application_by_id(client: TestClient) -> None:
    company = create_company(client)
    created = create_application(client, company["id"])

    response = client.get(f"/applications/{created['id']}")

    assert response.status_code == 200
    assert response.json()["position_title"] == "Backend Developer"


def test_missing_application_returns_404(client: TestClient) -> None:
    response = client.get("/applications/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}


def test_update_application_partially(client: TestClient) -> None:
    company = create_company(client)
    created = create_application(client, company["id"])

    response = client.patch(
        f"/applications/{created['id']}",
        json={"status": "interview", "notes": "Phone screen scheduled."},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["position_title"] == "Backend Developer"
    assert data["status"] == "interview"
    assert data["notes"] == "Phone screen scheduled."


def test_invalid_status_returns_422(client: TestClient) -> None:
    company = create_company(client)

    response = client.post(
        "/applications",
        json={
            "company_id": company["id"],
            "position_title": "Backend Developer",
            "status": "waiting",
        },
    )

    assert response.status_code == 422


def test_delete_application(client: TestClient) -> None:
    company = create_company(client)
    created = create_application(client, company["id"])

    response = client.delete(f"/applications/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_deleted_application_is_no_longer_returned(client: TestClient) -> None:
    company = create_company(client)
    created = create_application(client, company["id"])

    delete_response = client.delete(f"/applications/{created['id']}")
    get_response = client.get(f"/applications/{created['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404
