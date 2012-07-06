from datetime import datetime
import json
import unittest

from pypercube.cube import Cube
from pypercube.cube import Query
from pypercube.event import Event
from pypercube.expression import EventExpression
from pypercube.expression import Sum
from pypercube.metric import Metric
from pypercube.time_utils import yesterday
from pypercube.time_utils import STEP_1_MIN

from tests import MockResponse
from tests import mock_get


class TestCube(unittest.TestCase):
    def setUp(self):
        self.c = Cube('testing.com')

    def test_init(self):
        self.assertEqual(self.c.hostname, 'testing.com')
        self.assertEqual(self.c.port, 1081)
        self.assertEqual(self.c.api_version, "1.0")

    def test_url(self):
        self.assertEqual(self.c.get_base_url(), "http://testing.com:1081/1.0")

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


class TestQuery(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2012, 07, 06)

    def test_param_building(self):
        params = Query._build_params(start=yesterday(self.now))
        self.assertEqual(len(params), 1)
        self.assertEqual(params['start'], yesterday(self.now).isoformat())

        params = Query._build_params(start=yesterday(self.now), stop=self.now)
        self.assertEqual(len(params), 2)
        self.assertEqual(params['stop'], self.now.isoformat())

        params = Query._build_params(start=yesterday(self.now), stop=self.now,
                step=STEP_1_MIN)
        self.assertEqual(len(params), 3)
        self.assertEqual(params['step'], json.dumps(STEP_1_MIN))

        params = Query._build_params(start=yesterday(self.now), stop=self.now,
                step=STEP_1_MIN, limit=10)
        self.assertEqual(len(params), 4)
        self.assertEqual(params['limit'], 10)

    def test_init(self):
        base_url = 'http://test_base.com/api/1.0'
        path = 'event/get'
        q = Query(base_url, path, start=yesterday(self.now), stop=self.now,
                limit=5)
        self.assertEqual(len(q.params), 3)
        self.assertEqual(q.base_url, base_url)
        self.assertEqual(q.path, path)
