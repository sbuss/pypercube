import unittest

# Path hack.
import sys
import os
sys.path.insert(0, os.path.abspath('..'))


class MockResponse(object):
    def __init__(self, ok=None, status_code=None, content=None, json=None):
        self.ok = ok
        self.status_code = status_code
        self.content = content
        self.json = json


def mock_get(response):
    """Create a method that returns the expected response."""
    def _fake_get(self, expression):
        params = self.params.copy()
        params.update(expression=expression)
        path = "{base_url}/{path}".format(
                base_url=self.base_url,
                path=self.path,
                )
        response.url = path
        return response
    return _fake_get


def __main__(*args, **kwargs):
    unittest.main()
