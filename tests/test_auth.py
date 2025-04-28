from fastapi.testclient import TestClient
import faker
from main import app
import pytest
from httpx import ASGITransport, AsyncClient

client = TestClient(app)

fake = faker.Faker()
client.fake_user_email = fake.email()
client.fake_user_password = fake.password()
client.fake_user_name = fake.first_name()
client.new_user_id = 0
client.auth_token = ""


def test_signup():
    response = client.post("api/auth/signup",
                           json={"password": client.fake_user_password,
                                 "user_name": client.fake_user_name}
    )
    assert response.status_code == 201
    client.new_user_id = response.json()


# def test_login():
#     response = client.post("api/auth/login",
#                            data={"username": client.fake_user_email,
#                                  "password": client.fake_user_password}
#     )
#     assert response.status_code == 200
#     client.auth_token = response.json()['access_token']

#
@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(transport=ASGITransport(app=app)) as ac:
        response = await ac.post(
            "api/auth/login",
            data={"username": client.fake_user_email, "password": client.fake_user_password}
        )
        assert response.status_code == 200



def test_me():
    response = client.get("api/auth/me", headers={"Authorization": f"Bearer {client.auth_token}"})
    assert response.status_code == 200
    assert response.json() == client.new_user_id