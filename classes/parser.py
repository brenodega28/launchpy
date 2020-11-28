import yaml

from classes.system import System
from constants.templates import Templates


class Parser:
    @staticmethod
    def parse(data):
        systems = {}

        for sys_name, projects in data.items():
            system = System(sys_name)
            systems[sys_name] = system

            for proj_name, data in projects.items():
                commands = data.pop("commands", [])

                if "virtualenv" in data:
                    system.add_python_project(
                        proj_name, data["path"], data["virtualenv"]
                    )
                elif "template" in data:
                    system.add_project_instance(Templates.new(data))
                else:
                    system.add_project(proj_name, data["path"])

                for command in commands:
                    system.projects[proj_name].add_command(command)

        return systems

    @staticmethod
    def parse_file(file_name):
        with open(file_name) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            return Parser.parse(data)