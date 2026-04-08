# SQL Debugging OpenEnv

## Description

This environment simulates real-world SQL debugging tasks.

## Tasks

1. Easy: Retrieve all users
2. Medium: Apply filtering conditions
3. Hard: Perform joins across tables

## Action Space

- sql_query: string

## Observation Space

- problem
- db_schema
- last_error
- query_result

## Reward

- 1.0 → correct
- 0.5 → partial
- 0.0 → incorrect

## Setup

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
