from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from api.helpers import api_restrict_method
from helpers import resolve_repository, verify_github_hmac
from models import Branch, Commit, Push


@csrf_exempt
@resolve_repository
@api_restrict_method(['POST'])
@verify_github_hmac
def hook_url(request, repository):
    data = json.loads(request.body)
    commit, _ = Commit.objects.get_or_create(repository=repository, hash=data['after'])
    branch, _ = Branch.objects.get_or_create(repository=repository, ref=data['ref'], defaults={
        'name': data['ref'].split('/')[-1],
        'head': commit,
    })
    if branch.head != commit:
        Push.objects.create(repository=repository, before=branch.head, after=commit, branch=branch)
        branch.head = commit
        branch.save()
    return HttpResponse(json.dumps({'status':200}))