from contextlib import contextmanager
from django.core.management.base import BaseCommand, CommandError
import os
import pwd
import shutil
import tempfile

from task_manager.models import ScheduledTask


@contextmanager
def chdir_temporary_folder(folder_in):
    folder = tempfile.mkdtemp() if folder_in is None else folder_in
    old_folder = os.getcwd()
    os.chdir(folder)
    try:
        yield
    finally:
        os.chdir(old_folder)
        if folder_in is None:
            shutil.rmtree(folder)


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
        directory = scheduled_task.working_directory if scheduled_task.working_directory else None
        with chdir_temporary_folder(directory):
            pipe = os.popen(scheduled_task.task.execution + " " + scheduled_task.arguments)
            scheduled_task.output += "\n".join([x.decode('utf-8') for x in pipe.readlines()])
            pid, exit_status = os.wait()
            if exit_status & 0xF:
                # Error - process got killed
                return
            exit_status >>= 8
            if exit_status == 0:
                scheduled_task.status = ScheduledTask.COMPLETED
            elif exit_status & 0x80:
                scheduled_task.save()
                return  # If we have this status code then we should re-queue the task.
            else:
                scheduled_task.status = ScheduledTask.ERROR
            scheduled_task.save()