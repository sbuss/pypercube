import requests


class Query(object):
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
            if step in (q[0] for q in cls.STEP_CHOICES):
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
