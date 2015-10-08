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


@receiver(models.signals.post_save)
def build_tasks(sender, instance, created, *args, **kwargs):
    if created and sender == Push:
        repository = instance.repository
        tasks = RegisteredTask.objects.filter(assign_on_push=True, repository=repository)
        for task in tasks:
            if task.branch is None or task.branch == instance.branch:
                created = ScheduledTask(task=task.task, user=task.user, working_directory=task.working_directory,
                              arguments=" ".join((
                    repository.get_name(),
                    instance.branch.name,
                    instance.after.hash,
                )))
                created.save()
                TaskToPush(task=created, push=instance).save()