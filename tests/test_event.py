import json
import unittest

from pypercube.event import Event
from pypercube import time_utils


class TestEvent(unittest.TestCase):
    def test_field_names(self):
        self.assertEqual(Event.TYPE_FIELD_NAME, "type")
        self.assertEqual(Event.TIME_FIELD_NAME, "time")
        self.assertEqual(Event.DATA_FIELD_NAME, "data")

    def test_load_json(self):
        now = time_utils.now()
        yesterday = time_utils.yesterday()
        e1_json_str = '{"time":"' + yesterday.isoformat() + '",'\
                '"type":"timing", '\
                '"data":{"elapsed_ms":83.488,"params":{}}}'
        e2_json_str = '{"time":"' + now.isoformat() + '",'\
                '"type":"timing", '\
                '"data":{"elapsed_ms":134.321,"params":{}}}'
        e1 = Event('timing', yesterday, {'elapsed_ms': 83.488, 'params': {}})
        e2 = Event('timing', now, {'elapsed_ms': 134.321, 'params': {}})

        load_e1 = Event.from_json(e1_json_str)
        load_e2 = Event.from_json(e2_json_str)
        self.assertEqual(e1, load_e1)
        self.assertEqual(e2, load_e2)
        self.assertNotEqual(e1, load_e2)
        self.assertNotEqual(e2, load_e1)

    def test_generate_json(self):
        now = time_utils.now()
        json_str = '{"time": "' + now.isoformat() + '",'\
                '"type": "timing", '\
                '"data": {"elapsed_ms": 83.488, "params":{}}}'
        e1 = Event('timing', now, {'elapsed_ms': 83.488, 'params': {}})
        load_e1 = Event.from_json(json_str)
        self.assertEqual(e1, load_e1)
        self.assertEqual(e1.to_json(), json.loads(json_str))
        self.assertEqual(Event.from_json(e1.to_json()), e1)
        self.assertEqual(Event.from_json(e1.__str__()), e1)

    def test_time_parsing(self):
        now = time_utils.now()
        json_str = '{"time": "' + now.isoformat() + '",'\
                '"type": "timing", '\
                '"data": {"test": true}}'

        e1 = Event('timing', now, {'test': True})
        e2 = Event('timing', now.isoformat(), {'test': True})
        self.assertEqual(e1, e2)
        load_e1 = Event.from_json(json_str)
        self.assertEqual(load_e1, e1)
        self.assertEqual(load_e1, e2)
