import subprocess
import time
import pytest
import requests
import json
import re


def call_agent(prompt: str):
    url = "http://localhost:8000/prompt/"
    data = {
        "prompt": prompt
    }
    response = requests.post(url, json=data)
    return response.json()


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


with open("test_data/evaluation/ground_truths.json", "r") as f:
    ground_truths = json.load(f)

@pytest.mark.parametrize("ground_truth", ground_truths)
def test_ground_truth(ground_truth):
    response = call_agent(ground_truth["question"])
    response_text_cleaned = response["response"].strip().lower()

    present_keywords = [x for x in ground_truth["keywords"] if x.strip().lower() in response_text_cleaned]
    assert len(present_keywords) == len(ground_truth["keywords"])

    # for key_word in ground_truth["keywords"]:
    #     key_word = key_word.strip().lower()
    #     assert key_word in response_text_cleaned

    # for doc in ground_truth["source"]:
    #     assert doc in response["documents"]


with open("test_data/evaluation/hallucination_check.json", "r") as f:
    hallucination_checks = json.load(f)

@pytest.mark.parametrize("hallucination_check", hallucination_checks)
def test_hallucinations(hallucination_check):
    response = call_agent(hallucination_check["question"])
    assert response == "I am sorry I could not find any information related to your question."
