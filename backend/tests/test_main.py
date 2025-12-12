from fastapi.testclient import TestClient
from app.main import app
from app.settings import Settings
from app.database import get_db
from app.utils import validate_token
from datetime import datetime

client = TestClient(app)

SUCCESS_STATUS_CODE = 200
HEALTH_CHECK_RESPONSE = {'status': 'ok'}
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def test_health_check() -> None:
    """
    Test the health check endpoint.
    """
    response = client.get('/api/health')
    assert response.status_code == SUCCESS_STATUS_CODE
    assert response.json()['status'] == HEALTH_CHECK_RESPONSE['status']
    assert datetime.strptime(response.json()['timestamp'], DATE_FORMAT)

def test_get_all_users() -> None:
    """
    Test the get all users endpoint.
    """
    response = client.get('/api/users')
    assert response.status_code == SUCCESS_STATUS_CODE

# More tests