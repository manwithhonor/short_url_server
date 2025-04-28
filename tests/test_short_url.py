from fastapi.testclient import TestClient
from main import app
import pytest
from httpx import ASGITransport, AsyncClient

client = TestClient(app)

def test_read_main():
    response = client.get('api/')
    assert response.status_code == 200
    assert response.text == 'Welcome to Short URL Service (SUS)'

def test_short_url():
    response = client.post('api/short_url/', json={"full_url": "https://www.google.com/"})
    assert response.status_code == 201
    resp_json = response.json()

    response = client.get(f'api/short_url/{resp_json["id"]}' )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_short_url():
    async with AsyncClient(transport=ASGITransport(app=app)) as ac:
        response = await ac.post(
            "api/short_url/",
            json={"full_url": "https://www.google.com/"}
        )
        assert response.status_code == 200