from fastapi.testclient import TestClient
from app.main import app
from app.settings import Settings
from app.database import get_db
from app.utils import validate_token

client = TestClient(app)

def test_health_check():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

def test_get_all_users():
    response = client.get('/api/users')
    assert response.status_code == 200

# More tests