# Codveda Level 2 Task 3 — API Integration

A Python REST API integration project for the Codveda Technology Python Development Internship.

## Features

- Uses Python `requests` for HTTP GET requests.
- Fetches user data from a public REST API.
- Parses JSON responses and normalizes useful fields.
- Displays API data in a readable terminal table.
- Searches users by name, username, email, city, or company.
- Refreshes API data without restarting the application.
- Handles timeout, connection, HTTP, invalid JSON, and unexpected response errors.
- Includes automated unit tests with mocked API responses.

## API

Default endpoint:

`https://jsonplaceholder.typicode.com/users`

The application uses JSONPlaceholder as a public demo REST API.

## Setup

Create/activate a virtual environment if desired, then install the dependency:

```bash
python3 -m pip install -r requirements.txt
```

## Run

```bash
python3 api_explorer.py
```

## Test

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Project Structure

```
.
├── api_explorer.py
├── requirements.txt
├── README.md
└── tests/
    └── test_api_explorer.py
```

## Internship

**Program:** Codveda Technology — Python Development Internship  
**Level:** 2 — Intermediate  
**Task:** 3 — API Integration
