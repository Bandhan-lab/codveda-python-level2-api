"""Codveda Level 2 Task 3 - API Integration.

A small REST API data explorer that fetches public user data,
parses JSON responses, displays useful fields, and handles
common network/API errors gracefully.
"""

from __future__ import annotations

from typing import Any

import requests

DEFAULT_API_URL = "https://jsonplaceholder.typicode.com/users"
DEFAULT_TIMEOUT = 10


class APIError(Exception):
    """Raised when an API request or response cannot be processed."""


def fetch_data(url: str = DEFAULT_API_URL, timeout: int = DEFAULT_TIMEOUT) -> list[dict[str, Any]]:
    """Fetch JSON data from an API endpoint."""
    if not url.strip():
        raise ValueError("API URL cannot be empty.")
    if timeout <= 0:
        raise ValueError("Timeout must be greater than zero.")

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.Timeout as exc:
        raise APIError("The API request timed out. Please try again.") from exc
    except requests.exceptions.ConnectionError as exc:
        raise APIError("Could not connect to the API. Check your internet connection.") from exc
    except requests.exceptions.HTTPError as exc:
        raise APIError(f"API returned an HTTP error: {exc}") from exc
    except requests.exceptions.RequestException as exc:
        raise APIError(f"API request failed: {exc}") from exc

    try:
        payload = response.json()
    except ValueError as exc:
        raise APIError("The API returned invalid JSON data.") from exc

    if not isinstance(payload, list):
        raise APIError("Unexpected API response format. Expected a JSON list.")

    return payload


def normalize_users(users: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep only user records with the expected fields."""
    normalized: list[dict[str, Any]] = []

    for user in users:
        if not isinstance(user, dict):
            continue

        normalized.append(
            {
                "id": user.get("id", "N/A"),
                "name": str(user.get("name", "Unknown")),
                "username": str(user.get("username", "Unknown")),
                "email": str(user.get("email", "Unknown")),
                "city": str(user.get("address", {}).get("city", "Unknown"))
                if isinstance(user.get("address"), dict)
                else "Unknown",
                "company": str(user.get("company", {}).get("name", "Unknown"))
                if isinstance(user.get("company"), dict)
                else "Unknown",
            }
        )

    return normalized


def search_users(users: list[dict[str, Any]], keyword: str) -> list[dict[str, Any]]:
    """Search users by name, username, email, city, or company."""
    keyword = keyword.strip().lower()
    if not keyword:
        return users

    return [
        user
        for user in users
        if any(
            keyword in str(user.get(field, "")).lower()
            for field in ("name", "username", "email", "city", "company")
        )
    ]


def display_users(users: list[dict[str, Any]], heading: str = "API Results") -> None:
    """Display user records in a readable table."""
    print(f"\n{heading}")
    print("=" * 105)

    if not users:
        print("No matching users found.")
        return

    print(
        f"{'ID':<4} {'Name':<22} {'Username':<16} "
        f"{'Email':<30} {'City':<15} {'Company':<20}"
    )
    print("-" * 105)

    for user in users:
        print(
            f"{str(user['id']):<4} "
            f"{user['name'][:21]:<22} "
            f"{user['username'][:15]:<16} "
            f"{user['email'][:29]:<30} "
            f"{user['city'][:14]:<15} "
            f"{user['company'][:19]:<20}"
        )


def main() -> None:
    """Run the interactive API data explorer."""
    print("=" * 105)
    print("                         API DATA EXPLORER")
    print("=" * 105)
    print(f"Endpoint: {DEFAULT_API_URL}")
    print(f"Timeout: {DEFAULT_TIMEOUT} seconds")

    try:
        raw_users = fetch_data()
        users = normalize_users(raw_users)
    except (APIError, ValueError) as exc:
        print(f"Error: {exc}")
        return

    display_users(users, "Fetched Users")

    while True:
        print("\nOptions:")
        print("1. Search users")
        print("2. Refresh API data")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            keyword = input("Search keyword (name/email/city/company): ")
            matches = search_users(users, keyword)
            display_users(matches, "Search Results")
        elif choice == "2":
            try:
                users = normalize_users(fetch_data())
                display_users(users, "Refreshed API Data")
            except APIError as exc:
                print(f"Error: {exc}")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-3.")


if __name__ == "__main__":
    main()
