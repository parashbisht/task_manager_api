def test_tasks_require_auth(client):
    response = client.get("/tasks")
    assert response.status_code == 401


def test_create_task(client, auth_headers):
    response = client.post(
        "/tasks",
        json={"title": "Write tests", "description": "Cover all endpoints"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write tests"
    assert data["completed"] is False
    assert "owner_id" in data


def test_create_task_missing_title(client, auth_headers):
    response = client.post(
        "/tasks", json={"description": "No title here"}, headers=auth_headers
    )
    assert response.status_code == 422


def test_list_tasks(client, auth_headers):
    client.post("/tasks", json={"title": "Task One"}, headers=auth_headers)
    client.post("/tasks", json={"title": "Task Two"}, headers=auth_headers)

    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_by_id(client, auth_headers):
    created = client.post(
        "/tasks", json={"title": "Find me"}, headers=auth_headers
    ).json()

    response = client.get(f"/tasks/{created['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Find me"


def test_get_task_not_found(client, auth_headers):
    response = client.get("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_task(client, auth_headers):
    created = client.post(
        "/tasks", json={"title": "Old title"}, headers=auth_headers
    ).json()

    response = client.put(
        f"/tasks/{created['id']}",
        json={"title": "New title", "description": "Updated", "completed": False},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_complete_task(client, auth_headers):
    created = client.post(
        "/tasks", json={"title": "Finish me"}, headers=auth_headers
    ).json()

    response = client.patch(
        f"/tasks/{created['id']}/complete", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_complete_task_twice_conflicts(client, auth_headers):
    created = client.post(
        "/tasks", json={"title": "Finish me twice"}, headers=auth_headers
    ).json()
    client.patch(f"/tasks/{created['id']}/complete", headers=auth_headers)

    response = client.patch(
        f"/tasks/{created['id']}/complete", headers=auth_headers
    )
    assert response.status_code == 409


def test_delete_task(client, auth_headers):
    created = client.post(
        "/tasks", json={"title": "Delete me"}, headers=auth_headers
    ).json()

    response = client.delete(f"/tasks/{created['id']}", headers=auth_headers)
    assert response.status_code == 200

    check = client.get(f"/tasks/{created['id']}", headers=auth_headers)
    assert check.status_code == 404


def test_user_cannot_see_other_users_tasks(client):
    client.post(
        "/auth/signup", json={"email": "userA@example.com", "password": "pass12345"}
    )
    login_a = client.post(
        "/auth/login", data={"username": "userA@example.com", "password": "pass12345"}
    )
    headers_a = {"Authorization": f"Bearer {login_a.json()['access_token']}"}

    client.post(
        "/auth/signup", json={"email": "userB@example.com", "password": "pass12345"}
    )
    login_b = client.post(
        "/auth/login", data={"username": "userB@example.com", "password": "pass12345"}
    )
    headers_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}

    created = client.post(
        "/tasks", json={"title": "User A's task"}, headers=headers_a
    ).json()

    response = client.get(f"/tasks/{created['id']}", headers=headers_b)
    assert response.status_code == 404