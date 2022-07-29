import datetime
from django.core.management.base import BaseCommand
import os


def parseline(line):
    pass


def logwalk(tid):
    logdir= "./integration_logs/"
    logs_found = []

    for dirpath, dirnames, filenames in os.walk(logdir):
        folders = [dirpath + subdir for subdir in dirnames]
        for f in folders:
            for entry in os.scandir(f):
                if "log" in entry.path:
                    with open(entry.path) as fp:

                        inside_log = False
                        for line in fp:
                            ts, *elements = line.split("|")
                            if len(elements) > 0:
                                elements[0] = elements[0].replace(" ", "")

                            if not ts.startswith("20"):
                                index = ts.find("20")
                                ts = ts[index::]

                            if not list(elements):
                                if inside_log:
                                    logs_found[-1][1] += "{}".format(line)
                                continue

                            elif str(elements[0]) == str(tid):
                                logs_found.append([ts[0:-5], line])
                                inside_log = True

                            else:
                                inside_log = False

    logs_found = sorted(logs_found, key=lambda packet : datetime.datetime.strptime(packet[0], "%Y-%m-%d %H:%M:%S").date())
    for line in logs_found:
        print(line)


class Command(BaseCommand):
    help = "Parse logs for a celery task" + \
           "\"python manage.py clear -task 29837r928bc872 \" will show logs for task 29837r928bc872 if exists"

    def handle(self, *args, **options):
        timestamp, tid = None, None
        if options["task_id"]:

            tid = options["task_id"][0]

        if options["timestamp"]:
            timestamp = options["timestamp"]

        if tid is None and timestamp is None:
            self.stdout.write(self.style.ERROR("Missing task_id or task time"))
            return

        if tid:
            logwalk(tid)



    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-task', nargs=1, type=str, help="task id", dest="task_id")
        parser.add_argument('--time', nargs=1, type=str, help="timestamp of task", dest="timestamp")
        # parser.add_argument('-file', nargs=1, type=str, help="optional file output, enter D for <task_id>.txt",dest=file )
