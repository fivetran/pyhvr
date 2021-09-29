def _exception_from_packed_args(exception_cls, args=None, kwargs=None):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    return exception_cls(*args, **kwargs)


class PyhvrError(Exception):
    """
    The base exception class for Pyhvr exceptions.
    :ivar msg: The descriptive message associated with the error.
    """

    fmt = "An unspecified error occurred"

    def __init__(self, **kwargs):
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs

        if self.kwargs.get("status_code"):
            self.status_code = self.kwargs["status_code"]
        if self.kwargs.get("message"):
            message = self.kwargs["message"]
            if message.startswith("F_"):
                self.message = message[10:]
                self.error_code = message[:8]
            else:
                self.message = message
                self.error_code = None

    # __reduce__ is for pickling
    def __reduce__(self):
        return _exception_from_packed_args, (self.__class__, None, self.kwargs)


class RestError(PyhvrError):
    """Raised for any error returned from a REST call.
    :ivar status_code: HTTP status code
    :ivar message: Error message returned in HTTP payload
    """

    fmt = "{status_code}: {message}"


class LoginError(PyhvrError):
    """Login failed.`
    :ivar status_code: HTTP status code
    :ivar message: Error message returned in HTTP payload
    """

    fmt = "{status_code}: {message}"


class ConnectionError(PyhvrError):
    """HTTP request failed to execute`
    :ivar message: Text of the underlying rquests exception
    """

    fmt = "{message}"
