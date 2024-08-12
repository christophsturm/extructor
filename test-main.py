import pytest
from fastapi.testclient import TestClient
from main import app  # Make sure this matches your FastAPI app filename

client = TestClient(app)

def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert '<h1>Extruct Web Service</h1>' in response.text

def test_extract():
    # Using a known URL that should return some microformat data
    # canyon grail yay
    response = client.get('/extract?url=https%3A%2F%2Fwww.canyon.com%2Fde-at%2Fgravel-bikes%2Fperformance%2Fgrail%2Fcf-slx%2Fgrail-cf-slx-8-axs%2F3580.html')
    assert response.status_code == 200
    json = response.json()
    assert json is not None
    assert isinstance(json, list)
    # Check if at least one of the expected keys is in the response
    assert json[0].get("type") == "Product"

def test_extract_invalid_url():
    response = client.get('/extract?url=not_a_valid_url')
    assert response.status_code == 422  # Unprocessable Entity for invalid input