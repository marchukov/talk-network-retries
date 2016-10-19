#!/usr/bin/env python3
import http
import logging
import requests
import requests.packages.urllib3 as urllib3
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import MaxRetryError


URL = 'http://172.17.0.2/test.json'
TIMEOUT = 60  # Seconds
RETRY_PREFIX = 'http://'  # Protocol to retry
MAX_RETRIES = 3  # Number of retries
BACKOFF_FACTOR = 25  # Seconds


def naive_get():
    r = requests.get(URL)
    r.raise_for_status()
    return r.json()


def naive_get_timeout():
    r = requests.get(URL, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def naive_get_retry():
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
    session.mount(RETRY_PREFIX, adapter)
    r = session.get(URL, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def get_retry():
    session = requests.Session()
    retry = urllib3.util.Retry(total=MAX_RETRIES,
                               connect=MAX_RETRIES,
                               read=MAX_RETRIES)
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount(RETRY_PREFIX, adapter)
    r = session.get(URL, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def get_retry_backoff():
    session = requests.Session()
    retry = urllib3.util.Retry(total=MAX_RETRIES,
                               connect=MAX_RETRIES,
                               read=MAX_RETRIES,
                               backoff_factor=BACKOFF_FACTOR)
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount(RETRY_PREFIX, adapter)
    r = session.get(URL, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def get_retry_extended():
    retry = urllib3.util.Retry(total=MAX_RETRIES, connect=MAX_RETRIES, read=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR)

    def attempt(url, retry=retry):
        try:
            # this essentially creates a new connection pool per request :-(
            session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(max_retries=retry)
            session.mount(RETRY_PREFIX, adapter)
            req = requests.Request('GET', url).prepare()
            # would be nice just to pass retry here, but we cannot :-(
            r = session.send(req, timeout=TIMEOUT)
            r.raise_for_status()
#        except MaxRetryError:
#            raise
        except ConnectionError as e:
            #  increment() will return a new Retry() object
            retry = retry.increment(req.method, url, error=e)
            retry.sleep()
            logging.warning("Retrying (%r) after connection broken by '%r': '%s'", retry, e, url)
            return attempt(url, retry=retry)
        return r

    return attempt(URL).json()


def get_content_aware():
    retry = urllib3.util.Retry(total=MAX_RETRIES,
                               connect=MAX_RETRIES,
                               read=MAX_RETRIES,
                               backoff_factor=BACKOFF_FACTOR)

    def attempt(url, retry=retry):
        try:
            session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(max_retries=retry)
            session.mount(RETRY_PREFIX, adapter)
            req = requests.Request('GET', url).prepare()
            r = session.send(req, timeout=TIMEOUT)
            r.raise_for_status()
            j = r.json()
        # DEMO ONLY. TypeError is too wide to handle here
        except (ConnectionError, TypeError) as e:
            retry = retry.increment(req.method, url, error=e)
            retry.sleep()
            logging.warning("Retrying (%r) after connection broken by '%r': '%s'", retry, e, url)
            return attempt(url, retry=retry)
        return j

    return attempt(URL)


if __name__ == "__main__":
    http.client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_logger = logging.getLogger('requests.packages.urllib3')
    requests_logger.setLevel(logging.DEBUG)
    requests_logger.propagate = True
    print(get_content_aware())
