Use it like this:

```python
from datetime import datetime, timedelta

from pypercube.cube import Cube
from pypercube.event import EventExpression
from pypercube.filters import StartsWith, EQ
from pypercube.metrics import Sum
from pypercube.query import Query

# Build the Cube connection configuration
c = Cube('cube.mydomain.com')
# Set up some filters
f = [StartsWith('path', '/wetlab'), EQ('status', 200)]
# Query for an Event
e = EventExpression("timing", ["path", "elapsed_ms"], filters=f)
# f and e are quivalent to cube query syntax:
#   timing(path, elapsed_ms).re('path', '^/wetlab').eq('status', 200)
# Set up some time boundaries
start = datetime.utcnow() - timedelta(days=5)
step = Query.STEP_1_hour
# Fetch the matching events, returns Event objects
events = c.get(e, start=start, step=step)

# Find the average response time for all successful requests:
f = [EQ('status', 200)]
# Get the elapsed time of requests
e_time = EventExpression("timing", "elapsed_ms", filters=f)
# Get the number of requests
e_num = EventExpression("timing", filters=f)
m_time_sum = Sum(e_time)
m_request_count = Sum(e_num)
# Get a computed metric, returns Metric objects
metrics = c.get(m_time_sum / m_request_count, start=start, step=step)
```
