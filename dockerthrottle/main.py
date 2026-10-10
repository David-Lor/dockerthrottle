import time
from .temp import get_temp, get_host_cores
from .docker import DockerService
from .settings import Settings, load_settings


class DockerThrottle:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.docker = DockerService(self.settings)
        self.temp = 0
        self.last_temp = 0
        self.last_limit = self.settings.cpu_limit.max_cores
        self.containers = []

    def loop(self):
        self.temp = get_temp(self.settings.temperature)
        if self.temp is None or self.temp <= 0:
            print("Invalid temp:", self.temp)
            return

        self.containers = self.docker.get_containers()

        limit = self._calculate_limit()
        if limit is not None and limit != self.last_limit:
            self.docker.set_cpu_limit(self.containers, limit)

        temp_emoji = "="
        if self.temp > self.last_temp:
            temp_emoji = "🢁"
        elif self.temp < self.last_temp:
            temp_emoji = "🢃"

        limit_emoji = "="
        if limit is not None and limit > self.last_limit:
            limit_emoji = "🢃"
        elif limit is not None and limit < self.last_limit:
            limit_emoji = "🢁"

        print(f"Temp: {temp_emoji}{self.temp}°C, Limit: {limit_emoji}{self.last_limit}")
        self.last_temp = self.temp
        self.last_limit = limit

    def run(self):
        delay = self.settings.cpu_limit.delay
        while True:
            try:
                self.loop()
                time.sleep(delay)

            # except Exception as e:
            #     print(f"Error: {e}")
            #     time.sleep(delay)

            except (KeyboardInterrupt, InterruptedError, SystemExit):
                break

        # Teardown
        self._restore_max_cores()

    def _calculate_limit(self):
        if self.temp > self.settings.temperature.limit:
            return self._calculate_limit_over()
        if self.temp <= self.settings.temperature.limit:
            return self._calculate_limit_under()
        return None

    def _calculate_limit_over(self):
        new_limit = self.last_limit - self.settings.cpu_limit.step
        if new_limit < self.settings.cpu_limit.min_cores:
            new_limit = self.settings.cpu_limit.min_cores
        return new_limit

    def _calculate_limit_under(self):
        new_limit = self.last_limit + self.settings.cpu_limit.step
        if new_limit > self.settings.cpu_limit.max_cores:
            new_limit = self.settings.cpu_limit.max_cores
        return new_limit

    def _restore_max_cores(self):
        print("Restoring max cores to", self.settings.cpu_limit.max_cores)
        self.docker.set_cpu_limit(self.containers, self.settings.cpu_limit.max_cores)


def main():
    settings = load_settings()
    if settings.cpu_limit.max_cores <= 0:
        max_cores = get_host_cores()
        if max_cores > 0:
            print("Setting max cores to", max_cores)
            settings.cpu_limit.max_cores = max_cores

    app = DockerThrottle(settings)
    app.run()
