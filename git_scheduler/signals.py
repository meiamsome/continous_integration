from django.dispatch import receiver
from django.db.models.signals import post_save

from git.models import Push
from git_scheduler.models import RegisteredTask, TaskToPush, GitHubAccessToken
from task_manager.models import ScheduledTask


@receiver(post_save)
def build_tasks(sender, instance, created, *args, **kwargs):
    # Generate tasks on push
    if created and sender == Push:
        repository = instance.repository
        tasks = RegisteredTask.objects.filter(assign_on_push=True, repository=repository)
        for task in tasks:
            if task.branch is None or task.branch == instance.branch:
                created = ScheduledTask(task=task.task, user=task.user, working_directory=task.working_directory,
                                        submit_status=task.submit_status, arguments=" ".join((
                                            repository.get_name(),
                                            instance.branch.name,
                                            instance.after.hash,
                                        )))
                created.save()
                TaskToPush(task=created, push=instance).save()
    # Update git hub statuses
    if sender == TaskToPush:
        if created and instance.submit_status:
            update_github_status(instance)

    if sender == ScheduledTask:
        if not created:
            try:
                task_to_push = TaskToPush.objects.get(task=instance)
            except TaskToPush.DoesNotExist:
                pass
            else:
                update_github_status(task_to_push)


def update_github_status(tasktopush):
    if not tasktopush.submit_status:
        return
    repository = tasktopush.push.repository
    token = GitHubAccessToken.objects.filter(repositories__contains=repository).first()
    if token is not None:
        if tasktopush.task.status == ScheduledTask.QUEUED:
            state = 'pending'
        elif tasktopush.task.status == ScheduledTask.COMPLETED:
            state = 'success'
        elif tasktopush.task.status == ScheduledTask.ERROR:
            state = 'failure'
        else:
            return
        description = ""
        if tasktopush.task.status != ScheduledTask.QUEUED:
            description = tasktopush.task.output
        if len(description) > 100:
            description = description[:97] + "..."
        token.api_call('POST', '/repos/%s/statuses/%s' % (repository, tasktopush.push.after.hash), {
            'state': state,
            'description': description,
            'context': 'continuous-integration/git.meiamso.me',
        })