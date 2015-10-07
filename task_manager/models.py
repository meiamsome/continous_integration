from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=100)
    execution = models.TextField()
    is_safe = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


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

    def __unicode__(self):
        return u"'%s' scheduled. (%s)" % (self.task, self.get_status_display())