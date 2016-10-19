#!/usr/bin/env python3
import json
import http
import logging
import urllib3


URL = 'http://172.17.0.2/test.json'
TIMEOUT = 60  # Seconds
MAX_RETRIES = 3  # Number of retries
BACKOFF_FACTOR = 25  # Seconds


def urllib3_test():

    retry = urllib3.util.Retry(total=MAX_RETRIES, connect=MAX_RETRIES, read=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR)
    http = urllib3.PoolManager(retries=retry, timeout=TIMEOUT)

    def attempt(url, http=http, retry=retry):
        r = None
        try:
            r = http.request('GET', url, retries=retry)
        except Exception as e:
            retry = r.retries if r else retry
            retry = retry.increment('GET', url, error=e)
            retry.sleep()
            logging.warning("Retrying (%r) after connection broken by '%r': '%s'", retry, e, url)
            return attempt(url, retry=retry)
        return r

    return json.loads(attempt(URL, http).data.decode('utf-8'))


if __name__ == "__main__":
    http.client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_logger = logging.getLogger('requests.packages.urllib3')
    requests_logger.setLevel(logging.DEBUG)
    requests_logger.propagate = True
    print(urllib3_test())
