
from time import sleep
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_transcribe():
    files = {'file': ("example.flac", open('./example.flac', 'rb').read(), "audio/flac")}
    response = client.post("/transcribe", files=files)

    checksum = "424522392f1d790c335720b2ae6c92ba"
    assert response.status_code == 200
    assert response.json() == {"checksum": checksum}
    
    # sleep(1)
    response = client.get('/result/{}.srt'.format(checksum))

    assert response.status_code == 200