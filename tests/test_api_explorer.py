import unittest
from unittest.mock import Mock, patch

import requests

from api_explorer import (
    APIError,
    fetch_data,
    main,
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

    def test_fetch_data_request_error(self):
        with patch(
            "api_explorer.requests.get",
            side_effect=requests.exceptions.RequestException("request failed"),
        ):
            with self.assertRaisesRegex(APIError, "API request failed"):
                fetch_data()

    def test_fetch_data_http_error(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

        with patch("api_explorer.requests.get", return_value=response):
            with self.assertRaisesRegex(APIError, "HTTP error"):
                fetch_data()

    def test_fetch_data_4xx_http_error(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

        with patch("api_explorer.requests.get", return_value=response):
            with self.assertRaisesRegex(APIError, "HTTP error"):
                fetch_data()

    def test_fetch_data_5xx_http_error(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")

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
            fetch_data("https://example.com/api", timeout=0)

    def test_fetch_data_invalid_url_type(self):
        with self.assertRaisesRegex(ValueError, "API URL"):
            fetch_data(None)

    def test_fetch_data_invalid_timeout_type(self):
        with self.assertRaisesRegex(ValueError, "Timeout"):
            fetch_data(timeout="10")

    def test_fetch_data_invalid_timeout_value(self):
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            fetch_data(timeout=-1)

    def test_fetch_data_empty_response(self):
        response = Mock()
        response.json.return_value = []

        with patch("api_explorer.requests.get", return_value=response):
            self.assertEqual(fetch_data(), [])

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

    def test_normalize_users_rejects_non_dictionary_record(self):
        with self.assertRaisesRegex(APIError, "index 0.*object"):
            normalize_users(["bad-record"])

    def test_normalize_users_rejects_missing_required_field(self):
        user = self._valid_user()
        del user["email"]

        with self.assertRaisesRegex(APIError, "missing email"):
            normalize_users([user])

    def test_normalize_users_allows_missing_nested_values(self):
        user = self._valid_user()
        user["address"] = {}
        user["company"] = {}

        result = normalize_users([user])

        self.assertEqual(result[0]["city"], "Unknown")
        self.assertEqual(result[0]["company"], "Unknown")

    def test_normalize_users_rejects_invalid_nested_structures(self):
        user = self._valid_user()
        user["address"] = "not-an-object"

        with self.assertRaisesRegex(APIError, "address must be an object"):
            normalize_users([user])

    def test_normalize_users_rejects_missing_address_and_company(self):
        for field in ("address", "company"):
            user = self._valid_user()
            del user[field]

            with self.subTest(field=field):
                with self.assertRaisesRegex(APIError, f"missing {field}"):
                    normalize_users([user])

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

    def test_search_users_by_name_username_and_email(self):
        users = [self._search_user()]

        self.assertEqual(search_users(users, "alice"), users)
        self.assertEqual(search_users(users, "alice01"), users)
        self.assertEqual(search_users(users, "alice@example.com"), users)

    def test_search_users_whitespace_keyword(self):
        users = [self._search_user()]

        self.assertEqual(search_users(users, "   "), users)

    def test_search_users_invalid_users(self):
        with self.assertRaisesRegex(ValueError, "list"):
            search_users(None, "alice")
        with self.assertRaisesRegex(ValueError, "object"):
            search_users(["bad-record"], "alice")

    def test_search_users_invalid_keyword(self):
        users = [self._search_user()]

        with self.assertRaisesRegex(ValueError, "string"):
            search_users(users, None)
        with self.assertRaisesRegex(ValueError, "string"):
            search_users(users, 123)

    @staticmethod
    def _valid_user():
        return {
            "id": 1,
            "name": "Alice",
            "username": "alice01",
            "email": "alice@example.com",
            "address": {"city": "Bhubaneswar"},
            "company": {"name": "Tech Labs"},
        }

    @staticmethod
    def _search_user():
        return {
            "id": 1,
            "name": "Alice",
            "username": "alice01",
            "email": "alice@example.com",
            "city": "Bhubaneswar",
            "company": "Tech Labs",
        }

    @patch("api_explorer.fetch_data", return_value=[{
        "id": 1,
        "name": "Alice",
        "username": "alice01",
        "email": "alice@example.com",
        "address": {},
        "company": {},
    }])
    @patch("builtins.input", side_effect=EOFError)
    def test_main_handles_eof(self, mock_input, mock_fetch):
        with patch("builtins.print") as mock_print:
            main()

        mock_print.assert_any_call("\nExiting API Data Explorer.")

    @patch("api_explorer.fetch_data", return_value=[{
        "id": 1,
        "name": "Alice",
        "username": "alice01",
        "email": "alice@example.com",
        "address": {},
        "company": {},
    }])
    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_main_handles_keyboard_interrupt(self, mock_input, mock_fetch):
        with patch("builtins.print") as mock_print:
            main()

        mock_print.assert_any_call("\nExiting API Data Explorer.")


if __name__ == "__main__":
    unittest.main()
