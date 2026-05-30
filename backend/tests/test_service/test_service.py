from fastapi import status


async def test_get_services_by_company_id(client, auth_header, data_create_services):
    for data in data_create_services:
        resp = client.post("/api/v1/company/service/", json=data, headers=auth_header)

        assert resp.status_code == status.HTTP_201_CREATED

    resp = client.get("/api/v1/company/service/", headers=auth_header)

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json().get("services") is not None

    services = resp.json().get("services")

    for i in range(len(services)):
        assert services[i]["name"] == data_create_services[i]["name"]
        assert services[i]["price"] == data_create_services[i]["price"]
        assert services[i]["duration"] == data_create_services[i]["duration"]
        assert services[i]["description"] == data_create_services[i]["description"]


async def test_create_service(client, auth_header, data_create_service):
    resp = client.post(
        "/api/v1/company/service/", json=data_create_service, headers=auth_header
    )

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()["name"] == data_create_service["name"]
    assert resp.json()["price"] == data_create_service["price"]
    assert resp.json()["duration"] == data_create_service["duration"]
    assert resp.json()["description"] == data_create_service["description"]


async def test_get_service_by_id(client, auth_header, data_create_service):
    resp_create_service = client.post(
        "/api/v1/company/service/", json=data_create_service, headers=auth_header
    )

    assert resp_create_service.status_code == status.HTTP_201_CREATED

    resp = client.get(
        f"/api/v1/company/service/{resp_create_service.json()['id']}",
        headers=auth_header,
    )

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["name"] == data_create_service["name"]
    assert resp.json()["price"] == data_create_service["price"]
    assert resp.json()["duration"] == data_create_service["duration"]
    assert resp.json()["description"] == data_create_service["description"]


async def test_get_service_by_id_when_not_found(client, auth_header):
    resp = client.get("/api/v1/company/service/1000", headers=auth_header)

    assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_update_service_by_id(
    client, auth_header, data_create_service, data_update_service
):
    resp_create_service = client.post(
        "/api/v1/company/service/", json=data_create_service, headers=auth_header
    )

    assert resp_create_service.status_code == status.HTTP_201_CREATED

    resp_update_service = client.patch(
        f"/api/v1/company/service/{resp_create_service.json()['id']}",
        headers=auth_header,
        json=data_update_service,
    )

    assert resp_update_service.status_code == status.HTTP_200_OK
    assert resp_update_service.json()["name"] == data_update_service["name"]
    assert resp_update_service.json()["price"] == data_update_service["price"]
    assert resp_update_service.json()["duration"] == data_update_service["duration"]
    assert (
        resp_update_service.json()["description"] == data_update_service["description"]
    )


async def test_remove_service_by_id(client, auth_header, data_remove_service):
    resp_create_service = client.post(
        "/api/v1/company/service/", headers=auth_header, json=data_remove_service
    )

    assert resp_create_service.status_code == status.HTTP_201_CREATED

    resp = client.delete(
        f"/api/v1/company/service/{resp_create_service.json()['id']}",
        headers=auth_header,
    )

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["is_removed"]
