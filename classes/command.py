import os
import subprocess
import psutil

from threading import Thread

from constants.status import Status


class Command:
    def __init__(self, project: object, command: str):
        self.project = project
        self.command = f"cd {project.path} && {command}"
        self._thread = None
        self.process = None
        self.monitor = None
        self.status = Status.WAITING_TO_START

    def _run(self):
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
        )

        self.status = Status.RUNNING

        self.monitor = psutil.Process(os.getpid())

        while True:
            outLine = self.process.stdout.readline().rstrip()
            self.project.system.log(
                f"[bold purple]{self.project.name}[/bold purple]: {outLine}"
            )
            if self.process.poll() != None:
                self.status = Status.FINISHED
                self.project.check_commands()
                break

    def start(self):
        self.status = Status.STARTING
        self._thread = Thread(target=self._run).start()


class PythonCommand(Command):
    def __init__(self, project: object, command: str, virtualenv_folder: str = None):
        super().__init__(project, command)
        self.virtualenv_folder = virtualenv_folder

        if virtualenv_folder:
            self.command = f"cd {project.path} && {self.project.path}/{virtualenv_folder}/bin/python {command}"