from datetime import datetime, timedelta
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
    post_commit, _ = Commit.objects.get_or_create(repository=repository, hash=data['after'])
    pre_commit, _ = Commit.objects.get_or_create(repository=repository, hash=data['before'])
    t_string = data['head_commit']['timestamp']
    timezone = timedelta(hours=int(t_string[-5:-3]), minutes=int(t_string[-2:]))
    if t_string[-6] == '-':
        timezone = - timezone
    time = datetime.strptime(t_string[:-6], "%Y-%m-%dT%H:%M:%S") - timezone
    branch, _ = Branch.objects.get_or_create(repository=repository, ref=data['ref'], defaults={
        'name': data['ref'].split('/')[-1],
        'head': post_commit,
    })
    if branch.head != post_commit:
        Push.objects.create(repository=repository, before=pre_commit, after=post_commit, branch=branch, time=time)
        branch.head = post_commit
        branch.save()
    return HttpResponse(json.dumps({'status':200}))