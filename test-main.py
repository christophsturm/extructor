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
    response = client.get('/extract?url=https://schema.org/')
    assert response.status_code == 200
    assert response.json() is not None
    assert isinstance(response.json(), dict)
    # Check if at least one of the expected keys is in the response
    assert any(key in response.json() for key in ['json-ld', 'microdata', 'opengraph', 'microformat'])

def test_extract_invalid_url():
    response = client.get('/extract?url=not_a_valid_url')
    assert response.status_code == 422  # Unprocessable Entity for invalid input