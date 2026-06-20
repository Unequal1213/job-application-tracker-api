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
    source: str | None = "LinkedIn",
) -> dict[str, Any]:
    response = client.post(
        "/applications",
        json={
            "company_id": company_id,
            "position_title": position_title,
            "job_url": "https://example.com/jobs/backend",
            "status": status,
            "source": source,
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
        "API Developer",
        "Backend Developer",
    ]


def test_list_applications_limit_and_offset(client: TestClient) -> None:
    company = create_company(client)
    create_application(client, company["id"], position_title="Backend Developer")
    create_application(client, company["id"], position_title="API Developer")
    create_application(client, company["id"], position_title="Platform Developer")

    response = client.get(
        "/applications",
        params={
            "limit": 1,
            "offset": 1,
            "sort_by": "position_title",
            "sort_order": "asc",
        },
    )

    assert response.status_code == 200
    assert [item["position_title"] for item in response.json()] == ["Backend Developer"]


def test_list_applications_filters_by_status(client: TestClient) -> None:
    company = create_company(client)
    create_application(
        client,
        company["id"],
        position_title="Saved Role",
        status="saved",
    )
    create_application(
        client,
        company["id"],
        position_title="Interview Role",
        status="interview",
    )

    response = client.get("/applications", params={"status": "interview"})

    assert response.status_code == 200
    assert [item["position_title"] for item in response.json()] == ["Interview Role"]


def test_list_applications_filters_by_company_id(client: TestClient) -> None:
    first_company = create_company(client, name="Acme")
    second_company = create_company(client, name="Globex")
    create_application(client, first_company["id"], position_title="Acme Role")
    create_application(client, second_company["id"], position_title="Globex Role")

    response = client.get("/applications", params={"company_id": second_company["id"]})

    assert response.status_code == 200
    assert [item["position_title"] for item in response.json()] == ["Globex Role"]


def test_list_applications_filters_by_source(client: TestClient) -> None:
    company = create_company(client)
    create_application(
        client,
        company["id"],
        position_title="Referral Role",
        source="Referral",
    )
    create_application(
        client,
        company["id"],
        position_title="LinkedIn Role",
        source="LinkedIn",
    )

    response = client.get("/applications", params={"source": "Referral"})

    assert response.status_code == 200
    assert [item["position_title"] for item in response.json()] == ["Referral Role"]


def test_list_applications_default_sorting(client: TestClient) -> None:
    company = create_company(client)
    create_application(client, company["id"], position_title="Older Role")
    create_application(client, company["id"], position_title="Newer Role")

    response = client.get("/applications")

    assert response.status_code == 200
    assert [item["position_title"] for item in response.json()] == [
        "Newer Role",
        "Older Role",
    ]


def test_list_applications_ascending_sorting(client: TestClient) -> None:
    company = create_company(client)
    create_application(client, company["id"], position_title="Backend Developer")
    create_application(client, company["id"], position_title="API Developer")

    response = client.get(
        "/applications",
        params={"sort_by": "position_title", "sort_order": "asc"},
    )

    assert response.status_code == 200
    assert [item["position_title"] for item in response.json()] == [
        "API Developer",
        "Backend Developer",
    ]


def test_get_application_by_id(client: TestClient) -> None:
    company = create_company(client)
    created = create_application(client, company["id"])

    response = client.get(f"/applications/{created['id']}")

    assert response.status_code == 200
    assert response.json()["position_title"] == "Backend Developer"


def test_application_stats_with_no_applications(client: TestClient) -> None:
    response = client.get("/applications/stats")

    assert response.status_code == 200
    assert response.json() == {
        "total": 0,
        "saved": 0,
        "applied": 0,
        "interview": 0,
        "rejected": 0,
        "offer": 0,
    }


def test_application_stats_with_mixed_statuses(client: TestClient) -> None:
    company = create_company(client)
    create_application(client, company["id"], status="saved")
    create_application(client, company["id"], status="applied")
    create_application(client, company["id"], status="interview")
    create_application(client, company["id"], status="rejected")
    create_application(client, company["id"], status="offer")
    create_application(client, company["id"], status="offer")

    response = client.get("/applications/stats")

    assert response.status_code == 200
    assert response.json() == {
        "total": 6,
        "saved": 1,
        "applied": 1,
        "interview": 1,
        "rejected": 1,
        "offer": 2,
    }


def test_application_stats_update_after_deleting_application(
    client: TestClient,
) -> None:
    company = create_company(client)
    saved_application = create_application(client, company["id"], status="saved")
    create_application(client, company["id"], status="offer")

    delete_response = client.delete(f"/applications/{saved_application['id']}")
    stats_response = client.get("/applications/stats")

    assert delete_response.status_code == 204
    assert stats_response.status_code == 200
    assert stats_response.json() == {
        "total": 1,
        "saved": 0,
        "applied": 0,
        "interview": 0,
        "rejected": 0,
        "offer": 1,
    }


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


def test_invalid_status_filter_returns_422(client: TestClient) -> None:
    response = client.get("/applications", params={"status": "waiting"})

    assert response.status_code == 422


def test_invalid_sort_by_returns_422(client: TestClient) -> None:
    response = client.get("/applications", params={"sort_by": "company_id"})

    assert response.status_code == 422


def test_invalid_sort_order_returns_422(client: TestClient) -> None:
    response = client.get("/applications", params={"sort_order": "oldest"})

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
