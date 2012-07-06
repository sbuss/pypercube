from datetime import datetime
import json
import unittest

from pypercube.cube import Cube
from pypercube.cube import Query
from pypercube.event import Event
from pypercube.expression import EventExpression

from tests import MockResponse
from tests import mock_get


class TestEventExpressions(unittest.TestCase):
    def setUp(self):
        self.c = Cube('unittest')

    def test_no_matching_events(self):
        mock_response = MockResponse(ok=True, status_code='200',
                content="[]", json=[])
        Query.get = mock_get(mock_response)

        event = EventExpression('test')
        response = self.c.get_event(event, limit=10)
        self.assertEqual(len(response), 0)

    def test_single_matching_event(self):
        timestamp = datetime.utcnow()
        expected_content = '[{"time":"' + timestamp.isoformat() + '"}]'

        mock_response = MockResponse(ok=True, status_code='200',
                content=expected_content, json=json.loads(expected_content))
        Query.get = mock_get(mock_response)

        event = EventExpression('test')
        response = self.c.get_event(event, limit=1)
        self.assertEqual(len(response), 1)
        self.assertTrue(isinstance(response[0], Event))
        self.assertEqual(response[0].time, timestamp)

    def test_copy(self):
        e1 = EventExpression('request', ['path', 'elapsed_ms'])
        e2 = e1.copy()
        self.assertEqual(e1, e2)
        e1 = e1.eq('path', '/')
        e3 = e1.copy()
        self.assertNotEqual(e1, e2)
        self.assertEqual(e1, e3)
        self.assertNotEqual(e2, e3)

    def test_equality(self):
        e1 = EventExpression('request')
        e2 = EventExpression('request')
        self.assertEqual(e1, e2)
        e1 = EventExpression('request', 'path')
        self.assertNotEqual(e1, e2)
        e2 = EventExpression('request', 'path')
        self.assertEqual(e1, e2)
        e1 = EventExpression('request', ['path', 'elapsed_ms'])
        self.assertNotEqual(e1, e2)
        e2 = EventExpression('request', ['path', 'elapsed_ms'])
        self.assertEqual(e1, e2)
        e1 = EventExpression('request', ['path', 'elapsed_ms']).eq('path', '/')
        self.assertNotEqual(e1, e2)
        e2 = EventExpression('request', ['path', 'elapsed_ms']).eq('path', '/')
        self.assertEqual(e1, e2)
        e1 = EventExpression('request', ['path', 'elapsed_ms']).eq(
            'path', '/').gt('elapsed_ms', 500)
        self.assertNotEqual(e1, e2)
        e2 = EventExpression('request', ['path', 'elapsed_ms']).eq(
            'path', '/').gt('elapsed_ms', 500)
        self.assertEqual(e1, e2)
