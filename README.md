# 🌐 API Data Explorer

> **Codveda Technology — Python Development Internship**  
> **Level 2 · Task 3 — API Integration**

A polished Python command-line application that connects to a public REST API, retrieves live JSON data, validates and normalizes the response, and presents useful information in a clean terminal interface.

The project goes beyond a basic `requests.get()` example by including structured error handling, response validation, search, API refresh, and a **27-test automated test suite**.

---

## ✨ What It Does

**API Data Explorer** fetches user data from [JSONPlaceholder](https://jsonplaceholder.typicode.com/) and turns the raw API response into an easy-to-read terminal experience.

### Core capabilities

- 🔗 HTTP **GET** requests using `requests`
- 📦 JSON response parsing and validation
- 🧹 Normalization of API records
- 📊 Clean tabular terminal output
- 🔎 Search by name, username, email, city, or company
- 🔄 Refresh API data without restarting the application
- 🛡️ Validation for unexpected API response structures
- ⚡ Timeout and connection-error handling
- 🚨 HTTP 4xx/5xx error handling
- 🧩 Invalid JSON and malformed-response handling
- ⌨️ Friendly invalid-input handling
- 🛑 Clean Ctrl+C / Ctrl+D exit
- 🧪 **27 automated unit tests** using mocked API responses

---

## 🖥️ Application Flow

```text
                    ┌──────────────────────┐
                    │   API Data Explorer  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   HTTP GET Request   │
                    │      requests       │
                    └──────────┬───────────┘
                               │
                     ┌─────────▼─────────┐
                     │   JSON Response   │
                     └─────────┬─────────┘
                               │
                     ┌─────────▼─────────┐
                     │ Validate + Parse  │
                     └─────────┬─────────┘
                               │
                     ┌─────────▼─────────┐
                     │ Normalize Records │
                     └─────────┬─────────┘
                               │
                     ┌─────────▼─────────┐
                     │ Display / Search  │
                     │     / Refresh     │
                     └───────────────────┘
```

---

## 🎯 Codveda Requirements

| Requirement | Implementation |
|---|---|
| Use `requests` for a GET request | ✅ `requests.get()` |
| Retrieve data from an API | ✅ JSONPlaceholder Users API |
| Parse and display API data | ✅ JSON parsing + terminal table |
| Handle API errors | ✅ Timeout, connection, HTTP, JSON and validation errors |

The project also includes additional functionality to demonstrate stronger Python and API-handling practices.

---

## 🔌 API Used

**Default endpoint**

```text
https://jsonplaceholder.typicode.com/users
```

JSONPlaceholder is a public demo REST API intended for development and testing.

The application expects a JSON list of user records and validates the response before displaying it.

---

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python 3 | Application logic |
| 🌐 Requests | HTTP/API communication |
| 🧪 unittest | Automated testing |
| 🎭 unittest.mock | Mocking API responses |
| 📄 JSON | API response format |
| 💻 Terminal/CLI | User interface |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Bandhan-lab/codveda-python-level2-api.git
cd codveda-python-level2-api
```

### 2. Create a virtual environment

Recommended on Ubuntu/Debian-based systems:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python api_explorer.py
```

---

## 🎮 Using the Application

After the initial API request, the application provides:

```text
Options:
1. Search users
2. Refresh API data
3. Exit
```

### 🔎 Search

Search across:

- Name
- Username
- Email
- City
- Company

Search is case-insensitive.

### 🔄 Refresh

Fetch the latest response from the API without restarting the application.

### 🛡️ Error Handling

The application provides user-friendly messages for common problems such as:

- No internet connection
- Request timeout
- HTTP 4xx errors
- HTTP 5xx errors
- Invalid JSON
- Unexpected API response format
- Malformed API records
- Invalid user input

---

## 🧪 Testing

The project uses Python's built-in `unittest` framework.

Run the complete test suite with:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

### Current test coverage

```text
27 tests
27 passed
0 failed
```

The tests cover successful API requests, network failures, HTTP errors, malformed responses, input validation, normalization, search behavior, and clean CLI exits.

**Tests use mocked HTTP requests**, so the test suite does not depend on an external API being available.

---

## 📁 Project Structure

```text
codveda-python-level2-api/
│
├── api_explorer.py             # Main application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git exclusions
│
└── tests/
    └── test_api_explorer.py    # Automated test suite
```

---

## 🧠 What This Project Demonstrates

This project demonstrates practical Python development skills including:

- REST API integration
- HTTP request handling
- JSON parsing
- Data validation
- Exception handling
- Type-aware function design
- CLI application development
- Search/filter logic
- Automated testing
- Mocking external services
- Dependency management
- Git/GitHub workflow

---

## 📌 Project Status

**Status:** ✅ Completed

**Internship:** Codveda Technology — Python Development  
**Level:** 2 — Intermediate  
**Task:** 3 — API Integration

---

## 👨‍💻 Developer

**Bandhan Kumar Sahoo**  
B.Tech — CSE (AI & ML)  
GITA Autonomous College, Bhubaneswar, Odisha, India

Built as part of the **Codveda Technology Python Development Internship**.

---

## ⭐ Repository

If you find the project useful, consider giving the repository a star.

**GitHub:**  
https://github.com/Bandhan-lab/codveda-python-level2-api
