from django.db import models


class Task(models.Model):
    execution = models.TextField()
    is_safe = models.BooleanField(default=False)


class ScheduledTask(models.Model):
    COMPLETED = 1
    QUEUED = 0
    ERROR = -1

    task = models.ForeignKey(Task)
    arguments = models.TextField()
    user = models.CharField(max_length=32, null=True)
    status = models.SmallIntegerField(choices=(
        (1, 'Completed'),
        (0, 'Queued'),
        (-1, 'Error'),
    ), default=0)
    working_directory = models.TextField()
    output = models.TextField()