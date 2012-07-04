import types

from pypercube import filters


class EventExpression(object):
    def __init__(self, event_type, event_properties=None):
        """Create an Event expression.

        :param event_type: The type of the event to query for.
        :type event_type: str
        :param event_properties: Any properties to fetch from the event.
        :type event_properties: `str` or `list(str)`

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> print(request_time.event_type)
        request
        >>> print(request_time.event_properties)
        ['elapsed_ms']
        >>> print(request_time.eq('path', '/').gt('elapsed_ms', 100).lt(
        ...     'elapsed_ms', 1000))  # doctest:+NORMALIZE_WHITESPACE
        request(elapsed_ms).eq(path, "/").gt(elapsed_ms, 100).lt(elapsed_ms,
                1000)
        """
        self.event_type = event_type
        if event_properties:
            if isinstance(event_properties, types.StringTypes):
                event_properties = [event_properties]
        else:
            event_properties = []
        self.event_properties = event_properties
        self.filters = []

    def copy(self):
        """Copy an EventExpression

        >>> e1 = EventExpression('request', ['path', 'elapsed_ms'])
        >>> e2 = e1.copy()
        >>> e1 == e2
        True
        >>> e1 = e1.eq('path', '/')
        >>> e3 = e1.copy()
        >>> e1 == e2
        False
        >>> e1 == e3
        True
        >>> e2 == e3
        False
        """
        c = EventExpression(self.event_type, self.event_properties[:])
        c.filters = self.filters[:]
        return c

    def __eq__(self, other):
        """
        >>> e1 = EventExpression('request')
        >>> e2 = EventExpression('request')
        >>> e1 == e2
        True
        >>> e1 = EventExpression('request', 'path')
        >>> e1 == e2
        False
        >>> e2 = EventExpression('request', 'path')
        >>> e1 == e2
        True
        >>> e1 = EventExpression('request', ['path', 'elapsed_ms'])
        >>> e1 == e2
        False
        >>> e2 = EventExpression('request', ['path', 'elapsed_ms'])
        >>> e1 == e2
        True
        >>> e1 = EventExpression('request', ['path', 'elapsed_ms']).eq(
        ...     'path', '/')
        >>> e1 == e2
        False
        >>> e2 = EventExpression('request', ['path', 'elapsed_ms']).eq(
        ...     'path', '/')
        >>> e1 == e2
        True
        >>> e1 = EventExpression('request', ['path', 'elapsed_ms']).eq(
        ...     'path', '/').gt('elapsed_ms', 500)
        >>> e1 == e2
        False
        >>> e2 = EventExpression('request', ['path', 'elapsed_ms']).eq(
        ...     'path', '/').gt('elapsed_ms', 500)
        >>> e1 == e2
        True
        """
        return self.event_type == other.event_type and \
                len(self.event_properties) == len(other.event_properties) and \
                all((x == y) for (x, y) in \
                    zip(self.event_properties, other.event_properties)) and \
                self.event_properties == other.event_properties and \
                len(self.filters) == len(other.filters) and \
                all((x == y) for (x, y) in zip(self.filters, other.filters))

    def eq(self, event_property, value):
        """An equals filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.eq('path', '/')
        >>> request_time == filtered
        False
        >>> len(request_time.filters)
        0
        >>> len(filtered.filters)
        1
        >>> print(filtered)
        request(elapsed_ms).eq(path, "/")
        """
        c = self.copy()
        c.filters.append(filters.EQ(event_property, value))
        return c

    def ne(self, event_property, value):
        """A not-equal filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.ne('path', '/')
        >>> print(filtered)
        request(elapsed_ms).ne(path, "/")
        """
        c = self.copy()
        c.filters.append(filters.NE(event_property, value))
        return c

    def lt(self, event_property, value):
        """A less-than filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.lt('elapsed_ms', 500)
        >>> print(filtered)
        request(elapsed_ms).lt(elapsed_ms, 500)
        """
        c = self.copy()
        c.filters.append(filters.LT(event_property, value))
        return c

    def le(self, event_property, value):
        """A less-than-or-equal-to filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.le('elapsed_ms', 500)
        >>> print(filtered)
        request(elapsed_ms).le(elapsed_ms, 500)
        """
        c = self.copy()
        c.filters.append(filters.LE(event_property, value))
        return c

    def gt(self, event_property, value):
        """A greater-than filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.gt('elapsed_ms', 500)
        >>> print(filtered)
        request(elapsed_ms).gt(elapsed_ms, 500)
        """
        c = self.copy()
        c.filters.append(filters.GT(event_property, value))
        return c

    def ge(self, event_property, value):
        """A greater-than-or-equal-to filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.ge('elapsed_ms', 500)
        >>> print(filtered)
        request(elapsed_ms).ge(elapsed_ms, 500)
        """
        c = self.copy()
        c.filters.append(filters.GE(event_property, value))
        return c

    def re(self, event_property, value):
        """A regular expression filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.re('path', '[^A-Za-z0-9+]')
        >>> print(filtered)
        request(elapsed_ms).re(path, "[^A-Za-z0-9+]")
        """
        c = self.copy()
        c.filters.append(filters.RE(event_property, value))
        return c

    def startswith(self, event_property, value):
        """A starts-with filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.startswith('path', '/cube')
        >>> print(filtered)
        request(elapsed_ms).re(path, "^/cube")
        """
        c = self.copy()
        c.filters.append(filters.RE(event_property, "^{value}".format(
            value=value)))
        return c

    def endswith(self, event_property, value):
        """An ends-with filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.endswith('path', 'event/get')
        >>> print(filtered)
        request(elapsed_ms).re(path, ".*event/get$")
        """
        c = self.copy()
        c.filters.append(filters.RE(event_property, ".*{value}$".format(
            value=value)))
        return c

    def contains(self, event_property, value):
        """A string-contains filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.contains('path', 'event')
        >>> print(filtered)
        request(elapsed_ms).re(path, ".*event.*")
        """
        c = self.copy()
        c.filters.append(filters.RE(event_property, ".*{value}.*".format(
            value=value)))
        return c

    def in_array(self, event_property, value):
        """An in-array filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.in_array('path', '/event')
        >>> print(filtered)
        request(elapsed_ms).in(path, ["/", "e", "v", "e", "n", "t"])
        >>> filtered = request_time.in_array('path', ['/event', '/'])
        >>> print(filtered)
        request(elapsed_ms).in(path, ["/event", "/"])
        """
        c = self.copy()
        c.filters.append(filters.IN(event_property, value))
        return c

    def get_expression(self):
        event_type = self.event_type
        event_property = self.event_properties
        filters = self.filters

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

    def __str__(self):
        return self.get_expression()
