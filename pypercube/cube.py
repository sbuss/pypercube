import requests

from pypercube.event import Event
from pypercube.metric import Metric
from pypercube.time_utils import STEP_CHOICES


class Cube(object):
    def __init__(self, hostname, port=1081, api_version="1.0"):
        self.hostname = hostname
        self.port = port
        self.api_version = api_version

    ### Utility methods ###
    def get_base_url(self):
        """
        >>> c = Cube('cube.mydomain.com')
        >>> print(c.get_base_url())
        http://cube.mydomain.com:1081/1.0
        """
        return "http://{hostname}:{port}/{api}".format(
                hostname=self.hostname,
                port=self.port,
                api=self.api_version)

    ### Data access methods
    def _handle_response(self, response, obj):
        if response.ok and response.json is not None:
            return [obj.from_json(record) for record in response.json]
        elif not response.ok:
            raise InvalidQueryError({
                "status": response.status_code,
                "url": response.url})
        return response.content

    def get_event(self, event_expression, start=None, stop=None, limit=None):
        query = Query(self.get_base_url(), "event/get", start, stop, None,
                limit)
        r = query.get(event_expression)
        return self._handle_response(r, Event)

    def get_metric(self, metric_expression, start=None, stop=None, step=None,
            limit=None):
        query = Query(self.get_base_url(), "metric/get", start, stop, step,
                limit)
        r = query.get(metric_expression)
        return self._handle_response(r, Metric)


class Query(object):
    def __init__(self, base_url, path, start=None, stop=None, step=None,
            limit=None):
        self.base_url = base_url
        self.path = path
        self.params = Query._build_params(start, stop, step, limit)

    @classmethod
    def _format_time(cls, t):
        if hasattr(t, 'isoformat'):
            return t.isoformat()
        return t

    @classmethod
    def _build_params(cls, start=None, stop=None, step=None, limit=None):
        params = dict()
        if start:
            params['start'] = cls._format_time(start)
        if stop:
            params['stop'] = cls._format_time(stop)
        if step:
            if step in (q[0] for q in STEP_CHOICES):
                params['step'] = "{step}".format(step=step)
            else:
                raise ValueError("{step} is not a valid step. See "
                "{cls}.STEP_CHOICES".format(
                    step=step,
                    cls=cls.__name__))
        if limit:
            params['limit'] = limit
        return params

    def get(self, expression):
        params = self.params.copy()
        params.update(expression=expression)
        path = "{base_url}/{path}".format(
                base_url=self.base_url,
                path=self.path,
                )
        return requests.get(path, params=params)


class InvalidQueryError(Exception):
    pass
