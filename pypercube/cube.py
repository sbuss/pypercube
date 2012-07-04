import requests


class Cube(object):
    STEP_10_sec = long(1e4)
    STEP_1_min = long(6e4)
    STEP_5_min = long(3e5)
    STEP_1_hour = long(36e5)
    STEP_1_day = long(864e5)

    STEP_CHOICES = (
            (STEP_10_sec, "10 seconds"),
            (STEP_1_min, "1 minute"),
            (STEP_5_min, "5 minutes"),
            (STEP_1_hour, "1 hour"),
            (STEP_1_day, "1 day"))

    def __init__(self, hostname, port=1081, api_version="1.0"):
        self.hostname = hostname
        self.port = port
        self.api_version = api_version

    ### Utility methods ###
    def get_base_url(self):
        return "http://{hostname}:{port}/{api}".format(
                hostname=self.hostname,
                port=self.port,
                api=self.api_version)

    @classmethod
    def _format_time(cls, t):
        if hasattr(t, 'isoformat'):
            return t.isoformat()
        return t

    @classmethod
    def _build_params(cls, start=None, stop=None, step=None, limit=None,
            expression=None):
        params = dict()
        if start:
            params['start'] = cls._format_time(start)
        if stop:
            params['stop'] = cls._format_time(stop)
        if step:
            if step in (q[0] for q in cls.STEP_CHOICES):
                params['step'] = "{step}".format(step=step)
            else:
                raise ValueError("{step} is not a valid step. See "
                "{cls}.STEP_CHOICES".format(
                    step=step,
                    cls=cls.__name__))
        if limit:
            params['limit'] = limit
        if expression:
            params['expression'] = expression
        return params

    ### Data access methods
    def get(self, expression, start=None, stop=None, step=None, limit=None):
        params = self._build_params(start, stop, step, limit, expression)
        path = "{base_url}/{path}".format(
                base_url=self.get_base_url(),
                path=expression.path,
                )
        r = requests.get(path, params=params)
        print(r.url)
        if r.ok and r.json:
            return [expression.response_type.from_json(record) for \
                    record in r.json]
        elif not r.ok:
            raise InvalidQueryError({
                "status": r.status_code,
                "url": r.url})
        return r.content


class Expression(object):
    def __init__(self, expression, response_type, path):
        self.expression = expression
        self.response_type = response_type
        self.path = path

    def __str__(self):
        return "%s" % self.expression


class InvalidQueryError(Exception):
    pass
