from django.shortcuts import get_object_or_404
import hmac

from models import Repository


def resolve_repository(old_function):
    def handler(request, repository_name, *args, **kwargs):
        user_name, repository_name = repository_name.split('/')
        repository = get_object_or_404(Repository, owner__username=user_name, name=repository_name)
        return old_function(request, repository, *args, **kwargs)
    return handler


def verify_github_hmac(old_function):
    def handler(request, repository, *args, **kwargs):
        # TODO
        return old_function(request, repository, *args, **kwargs)
    return handler
