from fastapi import FastAPI
from pydantic import BaseModel
import requests
import sqlite3

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:latest"


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI-to-Oracle POC is running",
        "docs": "http://127.0.0.1:8000/docs"
    }


@app.post("/ask")
def ask(question: Question):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": f"""
You are a utility analytics assistant.

Answer the user's question in one concise business sentence.

Question:
{question.question}
""",
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    answer = response.json()["response"]

    return {
        "question": question.question,
        "answer": answer
    }


@app.get("/meter-count")
def meter_count():
    conn = sqlite3.connect("meter_connections_demo.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM meter_connections
    """)

    count = cursor.fetchone()[0]
    conn.close()

    prompt = f"""
You are a utility business analyst.

Convert this database result into one concise business sentence.

Metric: Total meter connections
Result: {count}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    summary = response.json()["response"]

    return {
        "metric": "total_meter_connections",
        "count": count,
        "summary": summary
    }


@app.get("/monthly-meter-connections")
def monthly_meter_connections(year: int = 2026, month: int = 1):
    conn = sqlite3.connect("meter_connections_demo.db")
    cursor = conn.cursor()

    start_date = f"{year}-{month:02d}-01"

    if month == 12:
        end_date = f"{year + 1}-01-01"
    else:
        end_date = f"{year}-{month + 1:02d}-01"

    cursor.execute("""
        SELECT COUNT(*)
        FROM meter_connections
        WHERE connection_date >= ?
          AND connection_date < ?
    """, (start_date, end_date))

    count = cursor.fetchone()[0]
    conn.close()

    prompt = f"""
You are a utility business analyst.

Convert this result into one concise business sentence.

Metric: Monthly meter connections
Period: {year}-{month:02d}
Result: {count}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    summary = response.json()["response"]

    return {
        "metric": "monthly_meter_connections",
        "year": year,
        "month": month,
        "count": count,
        "summary": summary
    }