def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Write tests", "description": "Cover all endpoints"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write tests"
    assert data["completed"] is False
    assert "id" in data


def test_create_task_missing_title(client):
    response = client.post("/tasks", json={"description": "No title here"})
    assert response.status_code == 422


def test_list_tasks(client):
    client.post("/tasks", json={"title": "Task One"})
    client.post("/tasks", json={"title": "Task Two"})

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_by_id(client):
    created = client.post("/tasks", json={"title": "Find me"}).json()

    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find me"


def test_get_task_not_found(client):
    response = client.get("/tasks/9999")
    assert response.status_code == 404


def test_update_task(client):
    created = client.post("/tasks", json={"title": "Old title"}).json()

    response = client.put(
        f"/tasks/{created['id']}",
        json={"title": "New title", "description": "Updated", "completed": False},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_update_task_not_found(client):
    response = client.put(
        "/tasks/9999",
        json={"title": "Doesn't matter", "completed": False},
    )
    assert response.status_code == 404


def test_complete_task(client):
    created = client.post("/tasks", json={"title": "Finish me"}).json()

    response = client.patch(f"/tasks/{created['id']}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_complete_task_twice_conflicts(client):
    created = client.post("/tasks", json={"title": "Finish me twice"}).json()
    client.patch(f"/tasks/{created['id']}/complete")

    response = client.patch(f"/tasks/{created['id']}/complete")
    assert response.status_code == 409


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Delete me"}).json()

    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 200

    check = client.get(f"/tasks/{created['id']}")
    assert check.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/tasks/9999")
    assert response.status_code == 404