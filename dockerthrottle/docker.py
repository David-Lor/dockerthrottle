import subprocess

import fnmatch
from .settings import Settings

Container = str


class DockerService:
    def __init__(self, settings):
        self.settings: Settings = settings

    def get_containers(self):
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True, text=True, check=True)
            containers = result.stdout.strip().splitlines()
            filtered_containers = [
                c for c in containers
                if self._container_filter(c)
            ]
            return filtered_containers

        except Exception as e:
            print(f"Error getting containers: {e}")
            return []

    def set_cpu_limit(self, containers: list[Container], limit: float):
        for container in containers:
            try:
                subprocess.run(
                    ["docker", "update", "--cpus", str(limit), container],
                    stdout=subprocess.DEVNULL,
                    check=True,
                )
                # print(f"Set CPU limit for container {container} to {limit}")

            except Exception as e:
                print(f"Error setting CPU limit for container {container}: {e}")

    def _container_filter(self, container: Container):
        for container_fnmatch in self.settings.containers:
            if fnmatch.fnmatch(container, container_fnmatch):
                return True
        return False
