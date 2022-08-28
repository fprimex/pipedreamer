import collections
import copy
import inspect
import sys
import time

import requests
import six

if six.PY2:
    from httplib import responses
    from urlparse import urlsplit
else:
    from http.client import responses
    from urllib.parse import urlsplit

# Compatability with Python 3.10
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

from .pipedreamer_api import PipedreamAPI


def batch(sequence, callback, size=100, **kwargs):
    """Helper to setup batch requests.

    There are endpoints which support updating multiple resources at once,
    but they are often limited to 100 updates per request.
    This function helps with splitting bigger requests into sequence of
    smaller ones.

    Example:
        def add_organization_tag(organizations, tag):
            request = {'organizations': [
                {
                    'id': org['id'],
                    'tags': org['tags'] + [tag],
                } for org in organizations
            ]}
            job = z.organizations_update_many(request)['job_status']
            return job['id']

        # z = Pipedream(...)
        orgs = z.organizations_list(get_all_pages=True)['organizations']
        job_ids = [job for job in
                   batch(orgs, add_organization_tag, tag='new_tag')]

    Parameters:
        sequence - any sequence you want to split
        callback - function to call with slices of sequence,
            its return value is yielded on each slice
        size - size of chunks, combined with length of sequence determines
            how many times callback is called (defaults to 100)
        **kwargs - any additional keyword arguments are passed to callback
    """
    batch_len, rem = divmod(len(sequence), size)
    if rem > 0:
        batch_len += 1
    for i in range(batch_len):
        offset = i * size
        yield callback(sequence[offset:offset + size], **kwargs)


class PipedreamError(Exception):
    def __init__(self, msg, code, response):
        self.msg = msg
        self.error_code = code
        self.response = response

    def __str__(self):
        return repr('%s: %s %s' % (self.error_code, self.msg, self.response))


class AuthenticationError(PipedreamError):
    pass


class RateLimitError(PipedreamError):
    pass

ACCEPT_RETRIES = PipedreamError, requests.RequestException


class Pipedream(PipedreamAPI):
    """ Python API Wrapper for Pipedream"""

    def __init__(self, pipedreamer_oauth=None,
                 headers=None, client_args=None, api_version=1,
                 retry_on=None, max_retries=0):
        """
        Instantiates an instance of Pipedream. Takes optional parameters for
        HTTP Basic Authentication

        Parameters:
        pipedreamer_token - use oauth token for authentication
        headers - Pass headers in dict form. This will override default.
        client_args - Pass arguments to http client in dict form.
            {'allow_redirects': False, 'timeout': 2}
            or a common one is to disable SSL certficate validation
            {'verify': False}
        retry_on - Specify any exceptions from ACCEPT_RETRIES or non-2xx
            HTTP codes on which you want to retry request.
            Note that calling Pipedream.call with get_all_pages=True can make
            up to (max_retries + 1) * pages.
            Defaults to empty set, but can be any iterable, exception or int,
            which will become set with same values you provided.
        max_retries - How many additional connections to make when
            first one fails. No effect when retry_on evaluates to False.
            Defaults to 0.
        """
        # Set headers
        self.client_args = copy.deepcopy(client_args) or {}
        self.headers = copy.deepcopy(headers) or {}

        # Set attributes necessary for API
        self._pipedreamer_oauth = None

        self.client = requests.Session()

        self.pipedreamer_oauth = pipedreamer_oauth

        if api_version != 1:
            raise ValueError("Unsupported Pipedream API Version: %d" %
                             api_version)

        self._retry_on = {}
        self._max_retries = 0
        self.retry_on = retry_on
        self.max_retries = max_retries

    def _update_auth(self):
        if self._pipedreamer_oauth:
            self.client.auth = None
            self.headers['Authorization'] = 'Bearer ' + self.pipedreamer_oauth
        else:
            self.client.auth = None

    @property
    def pipedreamer_oauth(self):
        return self._pipedreamer_oauth

    @pipedreamer_oauth.setter
    def pipedreamer_oauth(self, value):
        self._pipedreamer_oauth = value
        self._update_auth()

    @pipedreamer_oauth.deleter
    def pipedreamer_oauth(self):
        self._pipedreamer_oauth = None
        self._update_auth()

    @property
    def retry_on(self):
        return self._retry_on

    @retry_on.setter
    def retry_on(self, value):
        if value is None:
            self._retry_on = set()
            return

        def _validate(v):
            exc = ("retry_on must contain only non-2xx HTTP codes"
                   "or members of %s" % (ACCEPT_RETRIES, ))

            if inspect.isclass(v):
                if not issubclass(v, ACCEPT_RETRIES):
                    raise ValueError(exc)
            elif isinstance(v, int):
                if 200 <= v < 300:
                    raise ValueError(exc)
            else:
                raise ValueError(exc)

        if isinstance(value, Iterable):
            for v in value:
                _validate(v)
            self._retry_on = set(value)
        else:
            _validate(value)
            self._retry_on = set([value])

    @retry_on.deleter
    def retry_on(self):
        self._retry_on = set()

    @property
    def max_retries(self):
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value):
        try:
            value = int(value)
            if value < 0:
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("max_retries must be non-negative integer")

        self._max_retries = value

    @max_retries.deleter
    def max_retries(self):
        self._max_retries = 0

    def call(self, path, query=None, method='GET', data=None,
             files=None, get_all_pages=False, complete_response=False,
             retry_on=None, max_retries=0, raw_query=None, retval=None,
             **kwargs):
        """Make a REST call to the Pipedream web service.

        Parameters:
        path - Path portion of the Pipedream REST endpoint URL.
        query - Query parameters in dict form.
        method - HTTP method to use in making the request.
        data - POST data or multi-part form data to include.
        files - Requests style dict of files for multi-part file uploads.
        get_all_pages - Make multiple requests and follow next_page.
        complete_response - Return raw request results.
        retry_on - Specify any exceptions from ACCEPT_RETRIES or non-2xx
            HTTP codes on which you want to retry request.
            Note that calling Pipedream.call with get_all_pages=True can make
            up to (max_retries + 1) * pages.
            Defaults to empty set, but can be any iterable, exception or int,
            which will become set with same values you provided.
        max_retries - How many additional connections to make when
            first one fails. No effect when retry_on evaluates to False.
            Defaults to 0.
        raw_query - Raw query string, starting with '?', that will be
            appended to the URL path and will completely override / discard
            any other query parameters. Enables use cases where query
            parameters need to be repeated in the query string.
        retval - Request a specific part of the returned response. Valid
            values are 'content', 'code', 'location', and 'headers'.
            JSON content is still automatically deserialized if possible.
            If retval is not specified, then the old behavior of trying
            to determine an appropriate value to return is used.
        """

        # Rather obscure way to support retry_on per single API call
        if retry_on and max_retries:
            try:
                _retry_on = self._retry_on
                _max_retries = self._max_retries

                self.retry_on = retry_on
                self.max_retries = max_retries
                return self.call(path=path,
                                 query=query,
                                 method=method,
                                 data=data,
                                 files=files,
                                 get_all_pages=get_all_pages,
                                 complete_response=complete_response)
            finally:
                self._retry_on = _retry_on
                self._max_retries = _max_retries

        # Support specifying a mime-type other than application/json
        mime_type = kwargs.pop('mime_type', 'application/json')

        for key in kwargs.keys():
            value = kwargs[key]
            if hasattr(value, '__iter__') and not isinstance(value, str):
                kwargs[key] = ','.join(map(str, value))

        if query:
            if kwargs:
                kwargs.update(query)
            else:
                kwargs = query

        if raw_query:
            path = path + raw_query
            kwargs = None

        url = 'https://api.pipedream.com/v1' + path

        if files:
            # Sending multipart file. data contains parameters.
            json = None
            self.headers.pop('Content-Type', None)
        elif (mime_type == 'application/json' and
                (method == 'POST' or method == 'PUT')):
            # Sending JSON data.
            json = data
            data = {}
            self.headers.pop('Content-Type', None)
        elif (mime_type != 'application/json' and
                (method == 'POST' or method == 'PUT')):
            # Uploading an attachment, probably.
            # Specifying the MIME type is required.
            json = None
            self.headers['Content-Type'] = mime_type
        else:
            # Probably a GET or DELETE. Not sending JSON or files.
            json = None
            self.headers.pop('Content-Type', None)

        all_requests_complete = False
        request_count = 0

        while not all_requests_complete:
            # Make an http request
            # counts request attempts in order to fetch this specific one
            request_count += 1
            try:
                response = self.client.request(method,
                                               url,
                                               params=kwargs,
                                               json=json,
                                               data=data,
                                               headers=self.headers,
                                               files=files,
                                               **self.client_args)
            except requests.RequestException:
                if request_count <= self.max_retries:
                    # we have to bind response to None in case
                    # self.client.request raises an exception and
                    # response holds old requests.Response
                    # (and possibly its Retry-After header)
                    response = None
                    self._handle_retry(response)
                    continue
                else:
                    raise

            # If the response status is not in the 200 range then assume an
            # error and raise proper exception

            code = response.status_code
            try:
                if not 200 <= code < 300 and code != 422:
                    if code == 401:
                        raise AuthenticationError(
                            response.content, code, response)
                    elif code == 429:
                        raise RateLimitError(
                            response.content, code, response)
                    else:
                        raise PipedreamError(
                            response.content, code, response)
            except PipedreamError:
                if request_count <= self.max_retries:
                    self._handle_retry(response)
                    continue
                else:
                    raise

            # Deserialize json content if content exists.
            # Also return false non strings (0, [], (), {})
            if response.content.strip() and 'json' in response.headers['content-type']:
                content = response.json()

                # set url to the next page if that was returned in the response
                url = content.get('next_page', None)
                # url we get above already has the start_time appended to it,
                # specific to incremental exports
                kwargs = {}
            elif response.content.strip() and 'text' in response.headers['content-type']:
                try:
                    content = response.json()
                    # set url to the next page if that was returned in the response
                    url = content.get('next_page', None)
                    # url we get above already has the start_time appended to it,
                    # specific to incremental exports
                    kwargs = {}
                except ValueError:
                    content = response.content
            else:
                content = response.content
                url = None

            if complete_response:
                return {
                    'response': response,
                    'content': content,
                    'status': response.status_code
                }

            else:
                if retval == 'content':
                    return content
                elif retval == 'code':
                    return response.status_code
                elif retval == 'location':
                    return response.headers.get('location')
                elif retval == 'headers':
                    return response.headers
                else:
                    # Attempt to automatically determine the value of
                    # most interest to return.

                    if response.headers.get('location'):
                        # Pipedream's response is sometimes the url of a newly
                        # created user/ticket/group/etc and they pass this through
                        # 'location'.  Otherwise, the body of 'content'
                        # has our response.
                        return response.headers.get('location')
                    elif content:
                        return content
                    else:
                        return response.status_code

        # Don't expect to ever make it here
        return result


    def _handle_retry(self, resp):
        """Handle any exceptions during API request or
        parsing its response status code.

        Parameters:
        resp: requests.Response instance obtained during concerning request
            or None, when request failed

        Returns: True if should retry our request or raises original Exception
        """
        exc_t, exc_v, exc_tb = sys.exc_info()

        if exc_t is None:
            raise TypeError('Must be called in except block.')

        retry_on_exc = tuple(
            (x for x in self._retry_on if inspect.isclass(x)))
        retry_on_codes = tuple(
            (x for x in self._retry_on if isinstance(x, int)))

        if issubclass(exc_t, PipedreamError):
            code = exc_v.error_code
            if exc_t not in retry_on_exc and code not in retry_on_codes:
                six.reraise(exc_t, exc_v, exc_tb)
        else:
            if not issubclass(exc_t, retry_on_exc):
                six.reraise(exc_t, exc_v, exc_tb)

        if resp is not None:
            try:
                retry_after = float(resp.headers.get('Retry-After', 0))
                time.sleep(retry_after)
            except (TypeError, ValueError):
                pass

        return True
