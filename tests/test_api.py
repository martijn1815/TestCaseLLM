import subprocess
import time
import pytest
import requests


@pytest.fixture(scope="session", autouse=True)
def docker_compose():
    # Start containers
    subprocess.run(
        ["docker-compose", "up", "-d"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3)
    yield
    # Stop containers
    subprocess.run(
        ["docker-compose", "down"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def test_prompt_endpoint():
    url = "http://localhost:8000/prompt/"
    data = {
        "prompt": "Test"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200


def test_feedback_endpoint():
    url = "http://localhost:8000/feedback/"
    data = {
        "conversation_id": "0",
        "feedback": "Test"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
