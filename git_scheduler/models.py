from django.db import models
from django.dispatch import receiver

from git.models import Push, Repository, Branch
from task_manager.models import Task, ScheduledTask


class RegisteredTask(models.Model):
    repository = models.ForeignKey(Repository)
    branch = models.ForeignKey(Branch, null=True, blank=True)
    task = models.ForeignKey(Task)
    user = models.CharField(max_length=32)
    assign_on_push = models.BooleanField(default=False)

    def __unicode__(self):
        name = u"Task on " + self.repository
        if self.branch is not None:
            name += u"/" + self.branch
        name += u": Executing '" + self.task + u"' as user '" + self.user + u"'"
        return name


@receiver(models.signals.post_save)
def build_tasks(sender, instance, created, *args, **kwargs):
    if created and sender == Push:
        repository = instance.repository
        tasks = RegisteredTask.objects.filter(assign_on_push=True, repository=repository)
        for task in tasks:
            if task.branch is None or task.branch == instance.branch:
                ScheduledTask(task=task.task, user=task.user, arguments=" ".join((
                    repository.get_name(),
                    instance.branch.name,
                    instance.after.hash,
                ))).save()