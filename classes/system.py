from classes.project import Project, PythonProject

import psutil
import os
import time
import datetime

from rich.console import Console
from rich.table import Table


from threading import Thread


class System:
    def __init__(self, name: str):
        self.name = name
        self.projects = {}
        self.history = []
        self.monitor = psutil.Process(os.getpid())

        self.log(f"Starting system {self.name}")

    def add_project_instance(self, project: Project):
        project.system = self
        self.projects[project.name] = project

    def add_project(self, name: str, path: str):
        self.projects[name] = Project(self, name, path)

    def add_python_project(self, name: str, path: str, virtualenv_folder: str):
        self.projects[name] = PythonProject(self, name, path, virtualenv_folder)

    def log(self, message):
        self.history.append(
            f"{datetime.datetime.now().strftime('%H:%M:%S')} - {message}"
        )

    def start(self):
        Thread(target=self.ui).start()

        for project in self.projects.values():
            self.log(f"Starting project {project.name}")
            project.start()

    def ui(self):

        while True:
            console = Console()
            table = Table(show_header=True, header_style="bold red")
            table.add_column("Name", width=12)
            table.add_column("Status")
            table.add_column("Info")
            table.add_column("CPU Usage (%)", justify="right")
            table.add_column("Memory Usage (%)", justify="right")

            table.add_row(
                "LaunchPy",
                "Running",
                f"Handling {len(self.projects)} projects.",
                str(self.monitor.cpu_percent(interval=1.0)) + "%",
                str(round(self.monitor.memory_percent() * 100)) + "%",
            )

            for project in self.projects.values():
                monitors = project.get_monitors()
                total_cpu = 0
                total_mem = 0

                for monitor in monitors:
                    if not monitor:
                        continue

                    total_cpu += monitor.cpu_percent(interval=0.2)
                    total_mem += round(monitor.memory_percent() * 100)

                table.add_row(
                    project.name,
                    project.status,
                    project.subtitle,
                    str(total_cpu) + "%",
                    str(total_mem) + "%",
                )

            os.system("clear")
            console.print(f"\n{self.name} System\n", style="bold red")
            console.print(table)

            console.print("\nOutputs: \n", style="bold green")
            for message in self.history[-5:]:
                console.print(message)

            time.sleep(0.2)
