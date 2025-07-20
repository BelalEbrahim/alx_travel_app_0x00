#!/usr/bin/env python3
"""
Unit and integration tests for client.GithubOrgClient
"""
import unittest
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    def test_org_google(self):
        """Test that org property calls get_json for 'google'."""
        with patch('client.get_json') as mock_get_json:
            mock_get_json.return_value = {'repos_url': 'url'}
            client = GithubOrgClient('google')
            self.assertEqual(client.org, mock_get_json.return_value)
            mock_get_json.assert_called_once_with(
                GithubOrgClient.ORG_URL.format(org='google')
            )

    def test_org_abc(self):
        """Test that org property calls get_json for 'abc'."""
        with patch('client.get_json') as mock_get_json:
            mock_get_json.return_value = {'repos_url': 'url'}
            client = GithubOrgClient('abc')
            self.assertEqual(client.org, mock_get_json.return_value)
            mock_get_json.assert_called_once_with(
                GithubOrgClient.ORG_URL.format(org='abc')
            )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the repos_url."""
        client = GithubOrgClient('org')
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock,
            return_value={'repos_url': 'my_url'}
        ):
            self.assertEqual(client._public_repos_url, 'my_url')

    def test_public_repos(self):
        """Test that public_repos returns repo names from payload."""
        payload = [
            {'name': 'repo1', 'license': {'key': 'k1'}},
            {'name': 'repo2', 'license': {'key': 'k2'}},
        ]
        with patch('client.get_json', return_value=payload) as mock_get_json:
            client = GithubOrgClient('org')
            with patch.object(
                GithubOrgClient,
                '_public_repos_url',
                new_callable=PropertyMock,
                return_value='url'
            ):
                repos = client.public_repos()
                self.assertEqual(repos, ['repo1', 'repo2'])
                mock_get_json.assert_called_once_with('url')

    def test_has_license(self):
        """Test has_license returns True if license matches, else False."""
        self.assertTrue(
            GithubOrgClient.has_license(
                {'license': {'key': 'my_license'}},
                'my_license'
            )
        )
        self.assertFalse(
            GithubOrgClient.has_license(
                {'license': {'key': 'other'}},
                'my_license'
            )
        )


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get to return fixture payloads."""
        cls.get_patcher = patch('utils.requests.get')
        mock_get = cls.get_patcher.start()
        mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    def test_get_patcher(self):
        """Test that get_patcher patches utils.requests.get."""
        self.assertEqual(
            self.get_patcher.attribute,
            'utils.requests.get'
        )

    def test_public_repos(self):
        """Test public_repos returns expected repos without license."""
        client = GithubOrgClient('org')
        self.assertEqual(
            client.public_repos(),
            self.expected_repos
        )

    def test_public_repos_with_license(self):
        """Test public_repos filters by license."""
        client = GithubOrgClient('org')
        self.assertEqual(
            client.public_repos(license='apache-2.0'),
            self.apache2_repos
        )
```(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests using fixtures."""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('client.get_json')
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = [cls.org_payload, cls.repos_payload]

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient('org')
        self.assertEqual(
            client.public_repos(),
            self.expected_repos
        )

    def test_public_repos_with_license(self):
        client = GithubOrgClient('org')
        self.assertEqual(
            client.public_repos(license='apache-2.0'),
            self.apache2_repos
        )


if __name__ == '__main__':
    unittest.main()