import json
import types

from dateutil import parser as date_parser


class Metric(object):
    TIME_FIELD_NAME = "time"
    VALUE_FIELD_NAME = "value"

    def __init__(self, time, value):
        """Build a Cube Metric.

        :param time: The timestamp of the metric.
        :type time: str or datetime
        :param data: The computer value for the metric.
        :type data: object
        """
        if isinstance(time, types.StringTypes):
            time = date_parser.parse(time, fuzzy=True)
        self.time = time
        self.value = value

    @classmethod
    def from_json(cls, json_obj):
        """Build a MetricResponse from JSON.

        :param json_obj: JSON data representing a Cube Metric.
        :type json_obj: `String` or `json`
        :throws: `InvalidMetricError` when any of {type,time,data} fields are
        not present in json_obj.
        """
        if isinstance(json_obj, str):
            json_obj = json.loads(json_obj)

        time = None
        value = None

        if cls.TIME_FIELD_NAME in json_obj:
            time = json_obj[cls.TIME_FIELD_NAME]
        else:
            raise InvalidMetricError("{field} must be present!".format(
                field=cls.TIME_FIELD_NAME))

        if cls.VALUE_FIELD_NAME in json_obj:
            value = json_obj[cls.VALUE_FIELD_NAME]

        return cls(time, value)

    def to_json(self):
        d = dict()
        d[self.TIME_FIELD_NAME] = self.time.isoformat()
        d[self.VALUE_FIELD_NAME] = self.value
        return d

    def __repr__(self):
        return "<Metric: {value}>".format(value=self)

    def __str__(self):
        return json.dumps(self.to_json())

    def __eq__(self, other):
        return self.time == other.time and \
                self.value == other.value


class InvalidMetricError(Exception):
    pass
