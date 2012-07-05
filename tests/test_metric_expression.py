from datetime import datetime
import json
import unittest

# Path hack.
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from pypercube.cube import Cube
from pypercube.cube import Query
from pypercube.metric import Metric
from pypercube.expression import EventExpression
from pypercube.expression import Sum

from tests import MockResponse
from tests import mock_get


class TestEventExpressions(unittest.TestCase):
    def setUp(self):
        self.c = Cube('unittest')

    def test_no_matching_metrics(self):
        mock_response = MockResponse(ok=True, status_code='200',
                content="[]", json=[])
        Query.get = mock_get(mock_response)

        event = EventExpression('test')
        metric = Sum(event)
        response = self.c.get_metric(metric, limit=10)
        self.assertEqual(len(response), 0)

    def test_single_matching_metric(self):
        timestamp = datetime.utcnow()
        expected_content = '[{"time":"' + timestamp.isoformat() + '", '\
                '"value":100}]'

        mock_response = MockResponse(ok=True, status_code='200',
                content=expected_content, json=json.loads(expected_content))
        Query.get = mock_get(mock_response)

        event = EventExpression('test')
        metric = Sum(event)
        response = self.c.get_metric(metric, limit=1)
        self.assertEqual(len(response), 1)
        self.assertTrue(isinstance(response[0], Metric))
        self.assertEqual(response[0].time, timestamp)
        self.assertEqual(response[0].value, 100)


if __name__ == "__main__":
    unittest.main()
