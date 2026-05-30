from fastapi import status


async def test_create_work_schedule(client, auth_header, data_create_work_schedule):
    resp = client.post(
        "/api/v1/company/work-schedule/",
        headers=auth_header,
        json=data_create_work_schedule,
    )

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["workSchedule"] == data_create_work_schedule["workSchedule"]


async def test_update_work_schedule(client, auth_header, data_update_work_schedule):
    resp = client.post(
        "/api/v1/company/work-schedule/",
        headers=auth_header,
        json=data_update_work_schedule,
    )

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["workSchedule"] == data_update_work_schedule["workSchedule"]


async def test_get_work_schedule(client, auth_header, data_update_work_schedule):
    resp = client.get("/api/v1/company/work-schedule/", headers=auth_header)

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["workSchedule"] == data_update_work_schedule["workSchedule"]
