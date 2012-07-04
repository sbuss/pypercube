from pypercube.query import Query


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

    def get(self, expression, start=None, stop=None, step=None, limit=None):
        query = Query(self.get_base_url(), expression.path, start=start,
                stop=stop, step=step, limit=limit)

        r = query.get(expression)
        print(r.url)
        if r.ok and r.json:
            return [expression.response_type.from_json(record) for \
                    record in r.json]
        elif not r.ok:
            raise InvalidQueryError({
                "status": r.status_code,
                "url": r.url})
        return r.content


class InvalidQueryError(Exception):
    pass
