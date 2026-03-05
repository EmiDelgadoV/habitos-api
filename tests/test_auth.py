def test_register_success(client):
    response = client.post("/auth/register", json={
        "username": "emi",
        "email": "emi@test.com",
        "password": "123456"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "emi"

def test_register_duplicate(client):
    client.post("/auth/register", json={
        "username": "emi",
        "email": "emi@test.com",
        "password": "123456"
    })
    response = client.post("/auth/register", json={
        "username": "emi",
        "email": "emi@test.com",
        "password": "123456"
    })
    assert response.status_code == 400

def test_login_success(client, registered_user):
    response = client.post("/auth/login", data={
        "username": registered_user["username"],
        "password": registered_user["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client, registered_user):
    response = client.post("/auth/login", data={
        "username": registered_user["username"],
        "password": "contrasenawrong"
    })
    assert response.status_code == 401