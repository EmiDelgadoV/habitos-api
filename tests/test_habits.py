def test_create_habit(client, auth_headers):
    response = client.post("/habits/", json={
        "name": "Leer",
        "description": "Leer 30 minutos"
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Leer"

def test_get_habits(client, auth_headers):
    client.post("/habits/", json={"name": "Leer"}, headers=auth_headers)
    response = client.get("/habits/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_update_habit(client, auth_headers):
    create = client.post("/habits/", json={"name": "Leer"}, headers=auth_headers)
    habit_id = create.json()["id"]
    response = client.put(f"/habits/{habit_id}", json={"name": "Leer 1 hora"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Leer 1 hora"

def test_delete_habit(client, auth_headers):
    create = client.post("/habits/", json={"name": "Leer"}, headers=auth_headers)
    habit_id = create.json()["id"]
    response = client.delete(f"/habits/{habit_id}", headers=auth_headers)
    assert response.status_code == 204

def test_habit_not_found(client, auth_headers):
    response = client.get("/habits/999/history", headers=auth_headers)
    assert response.status_code == 404