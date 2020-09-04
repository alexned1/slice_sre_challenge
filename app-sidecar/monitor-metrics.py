#!/usr/bin/env python3

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import polling

health_url = "http://app:4567/health"
status_ok = 200

requestLatencyValues = []
dbLatencyValues = []
cacheLatencyValues = []

timesCalled = 0


def poll_health():
    """Gets metrics from /health"""
    global timesCalled

    # Poll /health
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    response = session.get(health_url)

    # Check HTTP status code
    status_code = response.status_code
    if status_code != status_ok:
        exit(1)

    # Get metrics values
    metrics = response.json()['metrics']
    requestLatencyValues.append(metrics['requestLatency'])
    dbLatencyValues.append(metrics['dbLatency'])
    cacheLatencyValues.append(metrics['cacheLatency'])

    # If 60 seconds has passed, send data to STDOUT
    timesCalled += 1
    if timesCalled == 6:
        output_data()

        timesCalled = 0
        requestLatencyValues.clear()
        dbLatencyValues.clear()
        cacheLatencyValues.clear()

def output_data():
    """Calculates average, minimum and maximum of 
    metrics parameters. The resulting data is sent to
    STDOUT"""
    # Calculate average values
    avgRequestLatency = 0 if len(requestLatencyValues) == 0 else \
        sum(requestLatencyValues)/len(requestLatencyValues)
    avgDbLatency = 0 if len(dbLatencyValues) == 0 else \
        sum(dbLatencyValues)/len(dbLatencyValues)
    avgCacheLatency = 0 if len(cacheLatencyValues) == 0 else  \
        sum(cacheLatencyValues)/len(cacheLatencyValues)

    # Print values to STDOUT
    print("")
    print("Average Request Latency: ", avgRequestLatency)
    print("Average DB Latency: ", avgDbLatency)
    print("Average Cache Latency: ", avgCacheLatency)
    print("")
    print("Minimum Request Latency: ", min(requestLatencyValues))
    print("Minimum DB Latency: ", min(dbLatencyValues))
    print("Minimum Cache Latency: ", min(cacheLatencyValues))
    print("")
    print("Maximum Request Latency: ", max(requestLatencyValues))
    print("Maximum DB Latency: ", max(dbLatencyValues))
    print("Maximum Cache Latency: ", max(cacheLatencyValues))
    print("", flush=True)


# Execute poll_health() every 10 secs
polling.poll(lambda: poll_health(),
    step=10,
    poll_forever=True)