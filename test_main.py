
from time import sleep
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_transcribe():
    # file = open('./example.flac', 'rb')
    files = {'file': ("example.flac", open('example.flac', 'rb'), "audio/flac")}
    response = client.post("/transcribe", files=files)

    checksum = "424522392f1d790c335720b2ae6c92ba"
    assert response.status_code == 200
    assert response.json() == {"checksum": checksum}
    
    sleep(200)
    response = client.get('/result/{}'.format(checksum))

    assert response.status_code == 200