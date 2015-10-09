import base64
from django.db import models
import httplib
import json

from git.models import Push, Repository, Branch
from task_manager.models import Task, ScheduledTask


class RegisteredTask(models.Model):
    repository = models.ForeignKey(Repository)
    branch = models.ForeignKey(Branch, null=True, blank=True)
    task = models.ForeignKey(Task)
    user = models.CharField(max_length=32)
    assign_on_push = models.BooleanField(default=False)
    submit_status = models.BooleanField(default=False)
    working_directory = models.TextField()

    def __unicode__(self):
        name = u"Task on %s" % (self.repository, )
        if self.branch is not None:
            name += u"/%s" % (self.branch, )
        name += u": Executing '%s' as user '%s'" % (self.task, self.user)
        return name


class TaskToPush(models.Model):
    task = models.ForeignKey(ScheduledTask)
    push = models.ForeignKey(Push)
    submit_status = models.BooleanField(default=False)


class GitHubAccessToken(models.Model):
    username = models.CharField(max_length=100)
    token = models.CharField(max_length=40)
    repositories = models.ManyToManyField(Repository)

    def api_call(self, method, url, data=None):
        connection = httplib.HTTPSConnection('api.github.com')
        connection.request(method, url, json.dumps(data) if data is not None else None, {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": "Basic %s" % (
                base64.encodestring("%s:%s" % (self.username, self.token)).replace('\n',''),
            ),
            "User-Agent": self.username,  # Should be changed to an app name probably
        })
        response = connection.getresponse()
        return_value = ((response.status, response.reason), json.loads(response.read()))
        connection.close()
        return return_value