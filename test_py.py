from app import app, request

def test():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

