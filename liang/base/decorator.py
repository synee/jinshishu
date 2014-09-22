# -*- coding: utf-8 -*-
import functools
import datetime


def prep_params(**prep_kwargs):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(self, request, *args, **kwargs):
            for (k, v) in prep_kwargs.items():
                value = request.GET.get(k) or v
                kwargs[k] = value
            return fn(self, request, *args, **kwargs)

        return wrapper

    return decorator


def time_spend(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        time_start = datetime.datetime.now()
        result = fn(*args, **kwargs)
        time_end = datetime.datetime.now()
        print("%s: %s" % (str(fn), str((time_end - time_start).total_seconds() * 1000), ))
        return result

    return wrapper