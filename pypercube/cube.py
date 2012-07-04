import json
import types

from dateutil import parser as date_parser
import requests


class Event(object):
    """A Cube Event has a timestamp, a type, and a data dictionary."""

    TYPE_FIELD_NAME = "type"
    TIME_FIELD_NAME = "time"
    DATA_FIELD_NAME = "data"

    def __init__(self, type, time, data):
        """Create a Cube Event.

        :param type: The type of the event.
        :type type: str
        :param time: The timestamp of the event.
        :type time: str or datetime
        :param data: The data dictionary for the event.
        :type data: dict
        """
        self.type = type
        if isinstance(time, types.StringTypes):
            time = date_parser.parse(time, fuzzy=True)
        self.time = time
        self.data = data

    @classmethod
    def from_json(cls, json_obj):
        """Build an Event from JSON.

        :param json_obj: JSON data representing a Cube Event
        :type json_obj: `String` or `json`
        :throws: `InvalidEventError` when any of time field is not present
        in json_obj.
        """
        if isinstance(json_obj, str):
            json_obj = json.loads(json_obj)

        type = None
        time = None
        data = None
        if cls.TYPE_FIELD_NAME in json_obj:
            type = json_obj[cls.TYPE_FIELD_NAME]

        if cls.TIME_FIELD_NAME in json_obj:
            time = json_obj[cls.TIME_FIELD_NAME]
        else:
            raise InvalidEventError("{field} must be present!".format(
                field=cls.TIME_FIELD_NAME))

        if cls.DATA_FIELD_NAME in json_obj:
            data = json_obj[cls.DATA_FIELD_NAME]

        return cls(type, time, data)

    def to_json(self):
        d = dict()
        d[self.TYPE_FIELD_NAME] = self.type
        d[self.TIME_FIELD_NAME] = self.time.isoformat()
        d[self.DATA_FIELD_NAME] = self.data
        return json.dumps(d)

    def __str__(self):
        return self.to_json()


class MetricResponse(object):
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
            raise InvalidEventError("{field} must be present!".format(
                field=cls.TIME_FIELD_NAME))

        if cls.VALUE_FIELD_NAME in json_obj:
            value = json_obj[cls.VALUE_FIELD_NAME]

        return cls(time, value)

    def to_json(self):
        d = dict()
        d[self.TIME_FIELD_NAME] = self.time.isoformat()
        d[self.VALUE_FIELD_NAME] = self.value
        return json.dumps(d)

    def __str__(self):
        return self.to_json()


class InvalidEventError(Exception):
    pass


class Cube(object):
    def __init__(self, hostname, port=1081, api_version="1.0"):
        self.hostname = hostname
        self.port = port
        self.api_version = api_version

    ### Utility methods ###
    def _format_time(self, t):
        if hasattr(t, 'isoformat'):
            return t.isoformat()
        return t

    def get_base_url(self):
        return "http://{hostname}:{port}/{api}".format(
                hostname=self.hostname,
                port=self.port,
                api=self.api_version)

    def _build_params(self, start=None, stop=None, step=None, limit=None):
        params = dict()
        if start:
            params['start'] = self._format_time(start)
        if stop:
            params['stop'] = self._format_time(stop)
        if step:
            pass  # TODO
        if limit:
            params['limit'] = limit
        return params

    ### GET Events ###
    def _get_event_expression(self, event_type, event_property=None,
            filters=None):
        expression = "{event_type}".format(event_type=event_type)

        if event_property:
            if isinstance(event_property, types.StringTypes):
                p = event_property
            else:
                p = ",".join(str(x) for x in event_property)

            expression += "({properties})".format(properties=p)

        if filters:
            expression += "".join(str(filter) for filter in filters)

        return expression

    def get_event(self, event_type, event_property=None, filters=None,
            start=None, stop=None, limit=None):
        """Get an Event from Cube.

        :param event_type: The type of the event to query for.
        :type event_type: str
        :param filters: A list of filters to apply.
        :type filters: list(`Filter`)
        """

        params = self._build_params(start=start, stop=stop, limit=limit)
        params['expression'] = self._get_event_expression(
                event_type=event_type,
                event_property=event_property,
                filters=filters)

        path = "{base_url}/{path}".format(
                base_url=self.get_base_url(),
                path="event/get")

        r = requests.get(path, params=params)
        print(r.url)
        if r.ok and r.json:
            return [Event.from_json(record) for record in r.json]
        elif not r.ok:
            raise InvalidQueryError({
                "status": r.status_code,
                "url": r.url})
        return r.content

    ### POST Events ###
    # TODO

    ### GET Metrics ###
    def _get_metric_expression(self, metric, event_type,
            event_property=None, filters=None):
        expression = metric.apply(self._get_event_expression(
            event_type, event_property, filters))

        return expression

    def get_metric(self, metric, event_type, event_property=None,
            filters=None, start=None, stop=None, step=None, limit=None):
        params = self._build_params(start=start, stop=stop, step=step,
                limit=limit)
        params['expression'] = self._get_metric_expression(metric,
                event_type, event_property, filters)
        path = "{base_url}/{path}".format(
                base_url=self.get_base_url(),
                path="metric/get")

        r = requests.get(path, params=params)
        print(r.url)
        if r.ok and r.json:
            return [MetricResponse.from_json(record) for record in r.json]
        elif not r.ok:
            raise InvalidQueryError({
                "status": r.status_code,
                "url": r.url})
        return r.content


class InvalidQueryError(Exception):
    pass
