import types
import json
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
        return json.dumps(d)

    def __str__(self):
        return self.to_json()


class InvalidMetricError(Exception):
    pass


class MetricExpression(object):
    def __init__(self, expression):
        self.expression = "%s" % expression
        self.response_type = Metric
        self.path = "metric/get"

    def get_expression(self):
        return self.expression

    def __str__(self):
        return self.expression

    def _op(self, operator, right):
        return MetricExpression("{left} {operator} {right}".format(
            left=self,
            operator=operator,
            right=right))

    def __add__(self, right):
        return self._op("+", right)

    def __sub__(self, right):
        return self._op("-", right)

    def __mul__(self, right):
        return self._op("*", right)

    def __div__(self, right):
        return self._op("/", right)

    def __truediv__(self, right):
        return self.__div__(right)


class MetricOperation(MetricExpression):
    """A metric.

    When you add/subtract/multiply/divide two MetricOperations a new
    MetricExpression is returned."""
    def __init__(self, type, event):
        """A MetricOperation.

        :param type: The type of metric, eg 'sum' or 'min'
        :type type: str
        :param event: The EventExpression over which the metric calcuations
        will be performed.
        :type event: `pypercube.query.EventExpression`
        """
        self.type = type
        self.event = event
        super(MetricOperation, self).__init__(self.apply())

    def apply(self):
        return MetricExpression("{type}({value})".format(
                type=self.type,
                value=self.event))

    def __str__(self):
        return "%s" % self.apply()

    def __add__(self, right):
        return MetricExpression(self) + right

    def __sub__(self, right):
        return MetricExpression(self) - right

    def __mul__(self, right):
        return MetricExpression(self) * right

    def __div__(self, right):
        return MetricExpression(self).__div__(right)

    def __truediv__(self, right):
        return MetricExpression(self).__truediv__(right)


class Sum(MetricOperation):
    """A "sum" metric."""
    def __init__(self, event):
        super(Sum, self).__init__("sum", event)


class Min(MetricOperation):
    """A "min" metric."""
    def __init__(self, event):
        super(Min, self).__init__("min", event)


class Max(MetricOperation):
    """A "max" metric."""
    def __init__(self, event):
        super(Max, self).__init__("max", event)


class Median(MetricOperation):
    """A "median" metric."""
    def __init__(self, event):
        super(Median, self).__init__("median", event)


class Distinct(MetricOperation):
    """A "distinct" metric."""
    def __init__(self, event):
        super(Distinct, self).__init__("distinct", event)
