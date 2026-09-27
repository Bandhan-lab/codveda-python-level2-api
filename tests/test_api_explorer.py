import unittest
from unittest.mock import Mock, patch

import requests

from api_explorer import (
    APIError,
    fetch_data,
    normalize_users,
    search_users,
)


class TestAPIExplorer(unittest.TestCase):
    def test_fetch_data_success(self):
        response = Mock()
        response.json.return_value = [{"id": 1, "name": "Leanne Graham"}]

        with patch("api_explorer.requests.get", return_value=response) as mock_get:
            result = fetch_data("https://example.com/api", timeout=5)

        mock_get.assert_called_once_with("https://example.com/api", timeout=5)
        response.raise_for_status.assert_called_once()
        self.assertEqual(result, [{"id": 1, "name": "Leanne Graham"}])

    def test_fetch_data_timeout(self):
        with patch(
            "api_explorer.requests.get",
            side_effect=requests.exceptions.Timeout,
        ):
            with self.assertRaisesRegex(APIError, "timed out"):
                fetch_data()

    def test_fetch_data_connection_error(self):
        with patch(
            "api_explorer.requests.get",
            side_effect=requests.exceptions.ConnectionError,
        ):
            with self.assertRaisesRegex(APIError, "Could not connect"):
                fetch_data()

    def test_fetch_data_http_error(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

        with patch("api_explorer.requests.get", return_value=response):
            with self.assertRaisesRegex(APIError, "HTTP error"):
                fetch_data()

    def test_fetch_data_invalid_json(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.side_effect = ValueError("invalid json")

        with patch("api_explorer.requests.get", return_value=response):
            with self.assertRaisesRegex(APIError, "invalid JSON"):
                fetch_data()

    def test_fetch_data_unexpected_payload(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"users": []}

        with patch("api_explorer.requests.get", return_value=response):
            with self.assertRaisesRegex(APIError, "Expected a JSON list"):
                fetch_data()

    def test_fetch_data_validation(self):
        with self.assertRaises(ValueError):
            fetch_data("", timeout=10)
        with self.assertRaises(ValueError):
            fetch_data(DEFAULT_URL := "https://example.com/api", timeout=0)

    def test_normalize_users(self):
        raw = [
            {
                "id": 1,
                "name": "Leanne Graham",
                "username": "Bret",
                "email": "Sincere@april.biz",
                "address": {"city": "Gwenborough"},
                "company": {"name": "Romaguera-Crona"},
            },
            "bad-record",
        ]

        self.assertEqual(
            normalize_users(raw),
            [
                {
                    "id": 1,
                    "name": "Leanne Graham",
                    "username": "Bret",
                    "email": "Sincere@april.biz",
                    "city": "Gwenborough",
                    "company": "Romaguera-Crona",
                }
            ],
        )

    def test_search_users(self):
        users = [
            {
                "id": 1,
                "name": "Alice",
                "username": "alice01",
                "email": "alice@example.com",
                "city": "Bhubaneswar",
                "company": "Tech Labs",
            },
            {
                "id": 2,
                "name": "Bob",
                "username": "bob02",
                "email": "bob@example.com",
                "city": "Delhi",
                "company": "Code House",
            },
        ]

        self.assertEqual(len(search_users(users, "bhubaneswar")), 1)
        self.assertEqual(len(search_users(users, "TECH")), 1)
        self.assertEqual(search_users(users, ""), users)


if __name__ == "__main__":
    unittest.main()
