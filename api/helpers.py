from django.http import HttpResponseNotAllowed
import json


def api_restrict_method(request_types):
    def decorator(function):
        def handler(request, *args, **kwargs):
            if request.method not in request_types:
                return HttpResponseNotAllowed(request_types, json.dumps({
                    'status': 405,
                    'error': 'This endpoint does not support the method supplied.',
                    'supported_methods': request_types
                }))
            return function(request, *args, **kwargs)
        return handler
    return decorator