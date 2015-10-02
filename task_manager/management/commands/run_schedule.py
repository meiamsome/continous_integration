from django.core.management.base import BaseCommand, CommandError
import os
import pwd

from task_manager.models import ScheduledTask


class Command(BaseCommand):
    help = 'Runs the scheduled tasks that can be ran from the user'

    def handle(self, *args, **options):
        tasks = ScheduledTask.objects.filter(status=ScheduledTask.QUEUED)
        uid = os.getuid()
        if uid != 0:
            name = pwd.getpwuid(uid)[0]
            tasks.filter(user=name)
        else:
            # TODO
            return
        for scheduled_task in tasks:
            Command.run_task(scheduled_task)


    @staticmethod
    def run_task(scheduled_task):
        os.chdir(scheduled_task.working_directory)
        pipe = os.popen(scheduled_task.task.execution + " " + scheduled_task.arguments)
        scheduled_task.output = "\n".join(pipe.readlines())
        pid, exit_status = os.wait()
        if exit_status & 0xF:
            # Error
            pass
        exit_status >>= 8
        if exit_status == 0:
            scheduled_task.status = ScheduledTask.COMPLETED
        else:
            scheduled_task.status = ScheduledTask.ERROR
        scheduled_task.save()