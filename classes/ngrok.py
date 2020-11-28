from classes.command import Command
from constants.status import Status

import subprocess
import requests
import time
import json
import psutil

from threading import Thread


class Ngrok:
    def __init__(self, method: str, port: int, path: str = "~/"):
        self.name = "Ngrok"
        self.path = path
        self.method = method
        self.port = port
        self.command = f"cd ~/ && ./ngrok {method} {port}"
        self.status = Status.WAITING_TO_START
        self.subtitle = ""
        self.process = None
        self.monitor = None

    def get_processes(self):
        return [self.process]

    def get_monitors(self):
        return [self.monitor]

    def _run(self):
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
        )

        self.monitor = psutil.Process(self.process.pid)

        time.sleep(5)

        try:
            if self.method == "http":
                localhost_url = f"http://localhost:4040/api/tunnels"
                tunnel_url = requests.get(localhost_url).text
                j = json.loads(tunnel_url)
        except Exception as e:
            print(e)

        self.status = Status.RUNNING

        url = j["tunnels"][0]["public_url"]
        self.system.log(f"ngrok: serving url at {url}")
        self.subtitle = url

        while True:
            outLine = self.process.stdout.readline().rstrip()
            print(f"{self.name}: {outLine}")
            if self.process.poll() != None:
                self.status = Status.FINISHED
                break

    def start(self):
        self.status = Status.STARTING
        self._thread = Thread(target=self._run).start()
