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
    """Unit tests for GithubOrgClient methods"""


    @parameterized.expand([
        ('google',),
        ('abc',),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that org property calls get_json with correct URL"""
        mock_get_json.return_value = {'repos_url': 'url'}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, mock_get_json.return_value)
        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org_name)
        )


    def test_public_repos_url(self):
        """Test that _public_repos_url returns org['repos_url']"""
        client = GithubOrgClient('org')
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock,
            return_value={'repos_url': 'my_url'}
        ):
            self.assertEqual(client._public_repos_url, 'my_url')


    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names"""
        payload = [
            {'name': 'repo1', 'license': {'key': 'k1'}},
            {'name': 'repo2', 'license': {'key': 'k2'}},
        ]
        mock_get_json.return_value = payload
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


    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other'}}, 'my_license', False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests using fixtures"""


    @classmethod
    def setUpClass(cls):
        """Set up patcher for get_json and define side effects"""
        cls.get_patcher = patch('client.get_json')
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = [cls.org_payload, cls.repos_payload]


    @classmethod
    def tearDownClass(cls):
        """Stop get_json patcher"""
        cls.get_patcher.stop()


    def test_public_repos(self):
        """Test that public_repos returns expected repositories"""
        client = GithubOrgClient('org')
        self.assertEqual(
            client.public_repos(),
            self.expected_repos
        )


    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        client = GithubOrgClient('org')
        self.assertEqual(
            client.public_repos(license='apache-2.0'),
            self.apache2_repos
        )


if __name__ == '__main__':
    unittest.main()
