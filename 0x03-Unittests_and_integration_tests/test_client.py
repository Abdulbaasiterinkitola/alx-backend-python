#!/usr/bin/env python3
"""
Unit and integration tests for client module.
"""

from typing import Any, Dict
import unittest
from unittest.mock import patch, Mock, PropertyMock

from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """Test that GithubOrgClient.org returns the result of get_json."""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assert_called_once()

    def test_public_repos_url(self) -> None:
        """Test that _public_repos_url returns the repos_url from org payload."""
        client = GithubOrgClient("test")
        fake_org = {"repos_url": "https://api.github.com/orgs/test/repos"}
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mocked_org:
            mocked_org.return_value = fake_org
            self.assertEqual(client._public_repos_url, fake_org.get("repos_url"))

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """Test public_repos returns the list of repository names."""
        test_repo_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_repo_payload
        client = GithubOrgClient("test")
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mocked_url:
            mocked_url.return_value = "https://api.github.com/orgs/test/repos"
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mocked_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict[str, Any], license_key: str, expected: bool) -> None:
        """Test has_license returns True if repo contains the license key."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
                     [(fixtures.org_payload, fixtures.repos_payload,
                       fixtures.expected_repos, fixtures.apache2_repos)])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls) -> None:
        """Start patching requests.get to return payloads from fixtures."""
        cls.get_patcher = patch('requests.get')
        mocked_get = cls.get_patcher.start()

        def _get(url: str, *args, **kwargs) -> Mock:
            mock_resp = Mock()
            if url.endswith('/repos'):
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = cls.org_payload
            return mock_resp

        mocked_get.side_effect = _get

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test that public_repos returns the expected repository names."""
        client = GithubOrgClient(self.org_payload.get("login"))
        repos = client.public_repos()
        self.assertEqual(sorted(repos), sorted(self.expected_repos))

    def test_public_repos_with_license(self) -> None:
        """Test that filtering repositories by license key works as expected."""
        client = GithubOrgClient(self.org_payload.get("login"))
        apache2 = client.public_repos(license_key="apache-2.0")
        self.assertEqual(sorted(apache2), sorted(self.apache2_repos))