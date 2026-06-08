
# AI-to-Oracle POC

## Overview

This repository contains a Proof of Concept (POC) for a Natural Language Analytics Assistant that demonstrates how a user can interact with enterprise data using natural language.

The current implementation uses:

- FastAPI
- SQLite (local demo database)
- Ollama
- Llama 3
- Swagger/OpenAPI

The objective is to validate the orchestration workflow before integrating with Oracle and PCAI-hosted LLMs.

---

## Architecture

Current Local Architecture

User / Swagger UI
        ↓
     FastAPI
        ↓
     SQLite
        ↓
   Business Logic
        ↓
   Llama 3 (Ollama)
        ↓
 Plain-English Summary
        ↓
      Response

---

## Features

### 1. General LLM Question Answering

Endpoint:

POST /ask

Example Request:

```json
{
  "question": "What is a meter connection?"
}
```

Example Response:

```json
{
  "answer": "A meter connection refers to the physical linking of a utility meter..."
}
```

### 2. Total Meter Connections

Endpoint:

GET /meter-count

Functionality:

- Queries the SQLite database
- Calculates total meter connections
- Uses Llama 3 to generate a business-friendly summary

Example Response:

```json
{
  "metric": "total_meter_connections",
  "count": 5,
  "summary": "As of today, our organization has a total of 5 active meter connections."
}
```

### 3. Monthly Meter Connections

Endpoint:

GET /monthly-meter-connections

Parameters:

- year
- month

Example:

```text
/monthly-meter-connections?year=2026&month=1
```

Example Response:

```json
{
  "metric": "monthly_meter_connections",
  "year": 2026,
  "month": 1,
  "count": 3,
  "summary": "In January 2026, we connected three new meters to our utility services."
}
```

---

## Project Structure

```text
AI_Oracle_POC/
│
├── app.py
├── create_db.py
├── meter_connections_demo.db
├── schema_metadata.json
├── test_llama.py
├── test_connection.py
├── requirements.txt
└── README.md
```

---

## Installation

### Install Python Dependencies

```bash
pip install fastapi uvicorn requests pydantic
```

### Install Ollama

Download:

https://ollama.com/download

Install Llama 3:

```bash
ollama pull llama3
```

Verify:

```bash
ollama run llama3
```

---

## Run Database Setup

```bash
py create_db.py
```

---

## Run FastAPI

```bash
py -m uvicorn app:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Current Status

Completed:

- Local Llama 3 orchestration
- FastAPI integration
- SQLite integration
- Business summary generation
- Swagger testing

Validated Workflow:

User Request
      ↓
FastAPI
      ↓
SQLite Query
      ↓
Llama 3 Summary
      ↓
Business Response

---

## Future Enhancements

### Oracle Integration

Replace:

```python
sqlite3.connect(...)
```

with:

```python
oracledb.connect(...)
```

using read-only Oracle views.

### PCAI Integration

Replace:

```python
http://localhost:11434/api/generate
```

with:

```python
https://<PCAI_ENDPOINT>
```

using deployed PCAI-hosted models.

### NLP-to-SQL

Future workflow:

User Question
      ↓
LLM Generates SQL
      ↓
SQL Validation
      ↓
Oracle Query
      ↓
LLM Summary
      ↓
Business Response

### Enterprise Features

- Authentication
- Authorization
- Audit Logging
- Prompt Versioning
- SQL Governance
- Model Monitoring
- Active Directory Integration

---


