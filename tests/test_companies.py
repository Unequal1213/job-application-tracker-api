from typing import Any

from fastapi.testclient import TestClient


def create_company(
    client: TestClient,
    name: str = "Acme",
    website: str | None = "https://example.com",
    notes: str | None = "Promising backend team.",
) -> dict[str, Any]:
    response = client.post(
        "/companies",
        json={"name": name, "website": website, "notes": notes},
    )

    assert response.status_code == 201
    return response.json()


def test_create_company(client: TestClient) -> None:
    data = create_company(client)

    assert data["id"] == 1
    assert data["name"] == "Acme"
    assert data["website"] == "https://example.com"
    assert data["notes"] == "Promising backend team."


def test_list_companies(client: TestClient) -> None:
    create_company(client, name="Acme")
    create_company(client, name="Globex", website=None, notes=None)

    response = client.get("/companies")

    assert response.status_code == 200
    assert [company["name"] for company in response.json()] == ["Acme", "Globex"]


def test_get_company_by_id(client: TestClient) -> None:
    created = create_company(client)

    response = client.get(f"/companies/{created['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == "Acme"


def test_missing_company_returns_404(client: TestClient) -> None:
    response = client.get("/companies/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Company not found"}


def test_update_company_partially(client: TestClient) -> None:
    created = create_company(client)

    response = client.patch(
        f"/companies/{created['id']}",
        json={"notes": "Updated notes."},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Acme"
    assert data["website"] == "https://example.com"
    assert data["notes"] == "Updated notes."


def test_delete_company(client: TestClient) -> None:
    created = create_company(client)

    response = client.delete(f"/companies/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_deleted_company_is_no_longer_returned(client: TestClient) -> None:
    created = create_company(client)

    delete_response = client.delete(f"/companies/{created['id']}")
    get_response = client.get(f"/companies/{created['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404
