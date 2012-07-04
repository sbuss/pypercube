from pypercube.query import Query
from pypercube.event import Event
from pypercube.metrics import MetricResponse


class Cube(object):
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

    ### GET Events ###
    def get_event(self, event_expression, start=None, stop=None, limit=None):
        """Get an Event from Cube.

        :param event_type: The type of the event to query for.
        :type event_type: str
        :param filters: A list of filters to apply.
        :type filters: list(`Filter`)
        """
        query = Query(self.get_base_url(), "event/get", start=start,
                stop=stop, limit=limit)

        r = query.get(event_expression)
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
    def get_metric(self, metric, start=None, stop=None, step=None, limit=None):
        query = Query(self.get_base_url(), "metric/get", start=start,
                stop=stop, step=step, limit=limit)
        r = query.get(metric)
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
