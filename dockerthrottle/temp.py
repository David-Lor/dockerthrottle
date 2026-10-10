import subprocess
from .settings import TemperatureSettings


def get_temp(settings: TemperatureSettings) -> float|None:
    try:
        with open(settings.device, "r") as f:
            temp = int(f.read().strip())
            return temp / 1000

    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None


def get_host_cores() -> int:
    try:
        result = subprocess.run(["nproc", "--all"], capture_output=True, text=True, check=True)
        return int(result.stdout.strip())

    except Exception as e:
        print(f"Error getting host cores: {e}")
        return 0
