#!/usr/bin/env python3
"""
Unit tests for utils module.
"""

from typing import Any, Tuple, Dict
import unittest
from unittest.mock import Mock, patch

from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for utils.access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Dict, path: Tuple[str, ...], expected: Any) -> None:
        """Test that access_nested_map returns the expected value for valid inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Dict, path: Tuple[str, ...]) -> None:
        """Test that access_nested_map raises a KeyError with the expected message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Tests for utils.get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict) -> None:
        """Test get_json returns the payload and requests.get is called once with the URL."""
        mock_resp = Mock()
        mock_resp.json.return_value = test_payload
        with patch('requests.get', return_value=mock_resp) as mocked_get:
            result = get_json(test_url)
            mocked_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for utils.memoize decorator."""

    def test_memoize(self) -> None:
        """Test that a method decorated with @memoize calls the underlying method only once."""
        class TestClass:
            """Helper class for memoize tests."""

            def a_method(self) -> int:
                """Return a constant integer."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Return a_property value using a_method (to be memoized)."""
                return self.a_method()

        test_obj = TestClass()
        with patch.object(TestClass, 'a_method', return_value=42) as mocked:
            first = test_obj.a_property
            second = test_obj.a_property
            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mocked.assert_called_once()