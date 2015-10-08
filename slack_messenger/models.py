from django.db import models
from slackclient import SlackClient

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


class SlackAlerts(models.Model):
    bot = models.ForeignKey(SlackBot)
    repository = models.ForeignKey(Repository)
    branch = models.ForeignKey(Branch, blank=True)
    channel = models.CharField(max_length=100)

    def alert(self, message):
        client = self.bot.get_client()
        client.api_call('chat.postMessage', {
            'channel': self.channel,
            'username': self.bot.name,
            'text': message,
        })