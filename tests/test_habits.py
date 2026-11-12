from datetime import date
from app.routers.habits import calcular_racha


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


def test_racha_cruza_cambio_de_mes():
    logs = {date(2026, 12, 1), date(2026, 11, 30), date(2026, 11, 29)}
    assert calcular_racha(logs, date(2026, 12, 1)) == 3


def test_racha_cruza_cambio_de_anio():
    logs = {date(2027, 1, 1), date(2026, 12, 31)}
    assert calcular_racha(logs, date(2027, 1, 1)) == 2


def test_racha_es_cero_si_hoy_no_esta():
    logs = {date(2026, 11, 10)}
    assert calcular_racha(logs, date(2026, 11, 11)) == 0