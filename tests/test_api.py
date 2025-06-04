import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("OPENAI_API_KEY", "test")

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_calendar():
    response = client.get('/calendar')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

