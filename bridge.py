# Unittests and Integration Tests Project (0x03)

This guide includes all **unit** and **integration** test files using `unittest`, `unittest.mock`, and `parameterized` for the **0x03-Unittests\_and\_integration\_tests** directory.

---

## Directory Structure

```
0x03-Unittests_and_integration_tests/
├── client.py
├── fixtures.py
├── utils.py
├── #!/usr/bin/env python3
"""
Unit tests for utils module: access_nested_map, get_json, memoize.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch

from utils import access_nested_map, get_json, memoize



class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""


    @parameterized.expand([
        ({'a': 1}, ('a',), 1),
        ({'a': {'b': 2}}, ('a',), {'b': 2}),
        ({'a': {'b': 2}}, ('a', 'b'), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)


    @parameterized.expand([
        ({}, ('a',)),
        ({'a': 1}, ('a', 'b')),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[-1]))



class TestGetJson(unittest.TestCase):
    """Tests for get_json"""


    @parameterized.expand([
        ('http://example.com', {'payload': True}),
        ('http://holberton.io', {'payload': False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, url, payload, mock_get):
        mock_get.return_value.json.return_value = payload
        result = get_json(url)
        mock_get.assert_called_once_with(url)
        self.assertEqual(result, payload)



class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator"""


    def test_memoize(self):
        class TestClass:
            """TestClass for memoize"""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()

├── test_client.py
└── README.md
```

---

## 1. `test_utils.py`

```python
#!/usr/bin/env python3
"""
Unit tests for utils module: access_nested_map, get_json, memoize.
"""
import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import patch

class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""

    @parameterized.expand([
        ({{"a": 1}}, ("a",), 1),
        ({{"a": {{"b": 2}}}}, ("a",), {{"b": 2}}),
        ({{"a": {{"b": 2}}}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({{"a": 1}}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[-1]))

class TestGetJson(unittest.TestCase):
    """Tests for get_json"""

    @parameterized.expand([
        ("http://example.com", {{"payload": True}}),
        ("http://holberton.io", {{"payload": False}}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, url, payload, mock_get):
        mock_get.return_value.json.return_value = payload
        result = get_json(url)
        mock_get.assert_called_once_with(url)
        self.assertEqual(result, payload)

class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator"""

    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()

if __name__ == '__main__':
    unittest.main()
```

---

## 2. `test_client.py`

````python
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
```python
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
        mock_get_json.return_value = {'repos_url': 'url'}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, mock_get_json.return_value)
        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org_name)
        )

    def test_public_repos_url(self):
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
        test_payload = [
            {'name': 'repo1', 'license': {'key': 'k1'}},
            {'name': 'repo2', 'license': {'key': 'k2'}},
        ]
        mock_get_json.return_value = test_payload
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
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )

@parameterized_class(*TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests using fixtures"""

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
````

python
\#!/usr/bin/env python3
"""
Unit and integration tests for client.GithubOrgClient
"""
import unittest
from client import GithubOrgClient
from utils import get\_json, access\_nested\_map
from fixtures import TEST\_PAYLOAD
from parameterized import parameterized, parameterized\_class
from unittest.mock import patch, PropertyMock

class TestGithubOrgClient(unittest.TestCase):
"""Unit tests for GithubOrgClient methods"""

```
@parameterized.expand([
    ('google',),
    ('abc',),
])
@patch('client.get_json')
def test_org(self, org_name, mock_get_json):
    mock_get_json.return_value = {{'repos_url': 'url'}}
    client = GithubOrgClient(org_name)
    self.assertEqual(client.org, mock_get_json.return_value)
    mock_get_json.assert_called_once_with(
        GithubOrgClient.ORG_URL.format(org=org_name)
    )

def test_public_repos_url(self):
    client = GithubOrgClient('org')
    with patch.object(
        GithubOrgClient,
        'org',
        new_callable=PropertyMock,
        return_value={{'repos_url': 'my_url'}}
    ):
        self.assertEqual(client._public_repos_url, 'my_url')

@patch('client.get_json')
def test_public_repos(self, mock_get_json):
    test_payload = [
        {{'name': 'repo1', 'license': {{'key': 'k1'}}}},
        {{'name': 'repo2', 'license': {{'key': 'k2'}}}},
    ]
    mock_get_json.return_value = test_payload
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
    ({{'license': {{'key': 'my_license'}}}}, 'my_license', True),
    ({{'license': {{'key': 'other'}}}}, 'my_license', False),
])
def test_has_license(self, repo, license_key, expected):
    self.assertEqual(
        GithubOrgClient.has_license(repo, license_key),
        expected
    )
```

@parameterized\_class(\*TEST\_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
"""Integration tests using fixtures"""

```
@classmethod
def setUpClass(cls):
    cls.get_patcher = patch('client.get_json')
    mock_get = cls.get_patcher.start()
    # side effect: first call returns org_payload, second returns repos_payload
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
```

if **name** == '**main**':
unittest.main()

````

---

## 3. `README.md`
```markdown
# Unittests and Integration Tests (0x03)

## Setup

Ensure you have Python 3.7+ on Ubuntu 18.04 and install dependencies:

```bash
pip install requests parameterized
````

## Running Unit Tests

```bash
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
```

## Project Requirements

* Files must be executable and start with `#!/usr/bin/env python3`
* Use `pycodestyle` (v2.5) for style compliance
* All modules, classes, and functions must have docstrings
* All functions and coroutines are type-annotated

## Structure

* `utils.py`, `client.py`, `fixtures.py`: source modules
* `test_utils.py`, `test_client.py`: test suites

```
```
