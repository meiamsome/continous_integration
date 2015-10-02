from django.db import models
from django.dispatch import receiver

from git.models import Push, Repository
from task_manager.models import Task, ScheduledTask


class RegisteredTask(models.Model):
    repository = models.ForeignKey(Repository)
    task = models.ForeignKey(Task)
    user = models.CharField(max_length=32)
    assign_on_push = models.BooleanField(default=False)


@receiver(models.signals.post_save)
def build_tasks(sender, instance, created, *args, **kwargs):
    if created and sender == Push:
        repository = instance.repository
        tasks = RegisteredTask.objects.filter(assign_on_push=True, repository=repository)
        for task in tasks:
            ScheduledTask(task=task.task, user=task.user, arguments=" ".join((
                repository.get_name(),
                sender.branch.ref,
                instance.after.hash,
            ))).save()