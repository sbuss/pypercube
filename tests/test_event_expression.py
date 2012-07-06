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
