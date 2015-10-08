from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import post_save

from git.models import Push
from git_scheduler.models import RegisteredTask, TaskToPush
from task_manager.models import ScheduledTask
from slack_messenger.models import SlackAlert


@receiver(post_save)
def handle_task_save(sender, instance, created, *args, **kwargs):
    if sender == TaskToPush:
        if created:
            repository = instance.push.repository
            branch = instance.push.branch
            relevant_alerts = SlackAlert.objects.filter(Q(branch=branch) | Q(branch=None), repository=repository)
            if not relevant_alerts:
                return
            message = "Task '%s' assigned to commit %s on %s/%s" %\
                      (instance.task, instance.push.after, instance.push.repository, instance.push.branch)
            for alert in relevant_alerts:
                alert.alert(message)

    if sender == ScheduledTask:
        if not created:
            task_to_push = TaskToPush.objects.get(task=instance)
            repository = task_to_push.push.repository
            branch = task_to_push.push.branch
            relevant_alerts = SlackAlert.objects.filter(Q(branch=branch) | Q(branch=None), repository=repository)
            if not relevant_alerts:
                return
            message = "Task '%s' updated for commit %s on %s/%s.\nStatus: %s" %\
                      (instance, task_to_push.push.after, repository, branch, instance.get_status_display())
            if instance.status != ScheduledTask.QUEUED:
                message += "\nOutput:\n%s" % (instance.output, )
            for alert in relevant_alerts:
                alert.alert(message)