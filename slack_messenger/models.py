from django.db import models
from slackclient import SlackClient
import json

from git.models import Repository, Branch


# Create your models here.
class SlackBot(models.Model):
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    repositories = models.ManyToManyField(Repository)

    def get_client(self):
        if not hasattr(self, '__slack_client'):
            self.__slack_client = SlackClient(self.token)
        return self.__slack_client


class SlackAlert(models.Model):
    bot = models.ForeignKey(SlackBot)
    repository = models.ForeignKey(Repository)
    branch = models.ForeignKey(Branch, blank=True, null=True)
    channel = models.CharField(max_length=100)

    def alert(self, message):
        client = self.bot.get_client()
        channel = self.channel
        if channel[0] == '@':
            resp = json.loads(client.api_call('im.open', user=channel[1:]))
            try:
                channel = resp['channel']['id']
            except KeyError:
                pass
        client.api_call('chat.postMessage', channel=channel, username=self.bot.name,text=message)