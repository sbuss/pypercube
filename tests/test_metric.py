import json
import unittest

from pypercube.metric import Metric
from pypercube import time_utils


class TestMetric(unittest.TestCase):
    def test_field_names(self):
        self.assertEqual(Metric.TIME_FIELD_NAME, "time")
        self.assertEqual(Metric.VALUE_FIELD_NAME, "value")

    def test_load_json(self):
        now = time_utils.now()
        yesterday = time_utils.yesterday()
        m1_json_str = '{"time":"' + yesterday.isoformat() + '",'\
                '"value":12345}'
        m2_json_str = '{"time":"' + now.isoformat() + '",'\
                '"value":54321}'
        m1 = Metric(yesterday, 12345)
        m2 = Metric(now, 54321)

        load_m1 = Metric.from_json(m1_json_str)
        load_m2 = Metric.from_json(m2_json_str)
        self.assertEqual(m1, load_m1)
        self.assertEqual(m2, load_m2)
        self.assertNotEqual(m1, load_m2)
        self.assertNotEqual(m2, load_m1)

    def test_generate_json(self):
        now = time_utils.now()
        json_str = '{"time":"' + now.isoformat() + '",'\
                '"value":12345}'
        m1 = Metric(now, 12345)
        load_m1 = Metric.from_json(json_str)
        self.assertEqual(m1, load_m1)
        self.assertEqual(m1.to_json(), json.loads(json_str))
        self.assertEqual(Metric.from_json(m1.to_json()), m1)
        self.assertEqual(Metric.from_json(m1.__str__()), m1)

    def test_time_parsing(self):
        now = time_utils.now()
        json_str = '{"time":"' + now.isoformat() + '",'\
                '"value":12345}'
        m1 = Metric(now, 12345)
        m2 = Metric(now.isoformat(), 12345)
        self.assertEqual(m1, m2)
        load_m1 = Metric.from_json(json_str)
        self.assertEqual(load_m1, m1)
        self.assertEqual(load_m1, m2)
