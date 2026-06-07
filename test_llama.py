import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3:latest",
        "prompt": "Explain monthly meter connections in one short business sentence.",
        "stream": False
    },
    timeout=120
)

print(response.json()["response"])