Pypercube
=========

Pypercube is a Python library for interacting with the
[Cube](https://github.com/square/cube) REST API. Currently you can only GET
Event and Metric data.

Installation
------------
pip install pypercube

Usage
-----

Use it like this:

```python
from pypercube.cube import Cube
from pypercube.expression import EventExpression
from pypercube.expression import Sum
from pypercube import time_utils

# Build the Cube connection configuration
c = Cube('cube.mydomain.com')
# Query for an Event and filter it
e = EventExpression("timing", ["path", "elapsed_ms"]).startswith('path', '/api/').eq('status', 200)
# This is equivalent to the Cube query
#   timing(path, elapsed_ms).re('path', '^/api/').eq('status', 200)
# Set up some time boundaries
stop = time_utils.now()
start = time_utils.yesterday(stop)
step = time_utils.STEP_1_HOUR
# Fetch the matching events, returns Event objects
events = c.get_event(e, start=start, stop=stop, limit=10)

# Get the elapsed time of successful requests
e_time = EventExpression("timing", "elapsed_ms").eq('status', 200)
# Get the number of requests
e_num = EventExpression("timing").eq('status', 200)
# Get a computed metric, returns Metric objects
metrics = c.get_metric(Sum(e_time) / Sum(e_num), start=start, stop=stop, step=step)
```
