from classes.command import Command, PythonCommand
from constants.status import Status


class Project:
    def __init__(self, system: object, name: str, path: str):
        self.name = name
        self.path = path
        self.system = system
        self.commands = []
        self.status = Status.WAITING_TO_START
        self.subtitle = ""

    def add_command(self, command):
        self.commands.append(Command(self, command))

    def start(self):
        self.status = Status.STARTING
        for command in self.commands:
            command.start()

        self.status = Status.RUNNING
        self.system.log(f"{self.name} is now up")

    def get_processes(self):
        return map(lambda c: c.process, self.commands)

    def get_monitors(self):
        return map(lambda c: c.monitor, self.commands)

    def check_commands(self):
        if all(map(lambda c: c.status == Status.FINISHED, self.commands)):
            self.status = Status.FINISHED


class PythonProject(Project):
    def __init__(
        self, system: object, name: str, path: str, virtalenv_folder: str = None
    ):
        super().__init__(system, name, path)
        self.virtalenv_folder = virtalenv_folder

    def add_command(self, command):
        self.commands.append(PythonCommand(self, command, self.virtalenv_folder))