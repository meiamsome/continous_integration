from django.dispatch import receiver
from django.db.models.signals import post_save

from git.models import Push
from git_scheduler.models import RegisteredTask, TaskToPush
from task_manager.models import ScheduledTask


@receiver(post_save)
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