from datetime import datetime
import json
import unittest

from pypercube.cube import Cube
from pypercube.cube import Query
from pypercube.expression import Distinct
from pypercube.expression import EventExpression
from pypercube.expression import Max
from pypercube.expression import Median
from pypercube.expression import MetricExpression
from pypercube.expression import Min
from pypercube.expression import Sum
from pypercube.metric import Metric

from tests import MockResponse
from tests import mock_get


class TestMetricExpressions(unittest.TestCase):
    def setUp(self):
        self.c = Cube('unittest')
        self.e = EventExpression('request')

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

    def _test_op(self, op_str, op):
        m1 = MetricExpression(op_str, self.e)
        m2 = op(self.e)
        self.assertEqual(m1, m2)
        s = "{op}(request)".format(op=op_str)
        self.assertEqual("%s" % m1, s)
        self.assertEqual("%s" % m2, s)

    def test_sum(self):
        self._test_op("sum", Sum)

    def test_min(self):
        self._test_op("min", Min)

    def test_max(self):
        self._test_op("max", Max)

    def test_median(self):
        self._test_op("median", Median)

    def test_distinct(self):
        self._test_op("distinct", Distinct)

    def test_equality(self):
        e1 = EventExpression('request')
        m1 = MetricExpression('sum', e1)
        m2 = MetricExpression('sum', e1)
        self.assertEqual(m1, m2)

        e2 = EventExpression('other')
        m2 = MetricExpression('sum', e2)
        self.assertNotEqual(m1, m2)

        m1 = MetricExpression('sum', e2)
        self.assertEqual(m1, m2)

        m1 = MetricExpression('min', e2)
        self.assertNotEqual(m1, m2)

        m2 = MetricExpression('min', e2)
        self.assertEqual(m1, m2)

    def test_invalid_params(self):
        self.assertRaisesRegexp(ValueError,
                "Events for Metrics may only select a single event property",
                Sum, EventExpression('request', ['path', 'user_id']))
        self.assertRaises(TypeError, Sum)
