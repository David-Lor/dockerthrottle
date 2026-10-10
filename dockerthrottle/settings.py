import os
import yaml
import pydantic

SETTINGS_FILE = os.getenv("SETTINGS_FILE", "settings.yaml")


class TemperatureSettings(pydantic.BaseModel):
    limit: float = 80
    device: str  # TODO Default value?


class CpuLimitSettings(pydantic.BaseModel):
    min_cores: float = 1
    max_cores: float = 0
    step: float = 1
    delay: float = 1


class Settings(pydantic.BaseModel):
    temperature: TemperatureSettings = pydantic.Field(default_factory=TemperatureSettings)
    cpu_limit: CpuLimitSettings = pydantic.Field(default_factory=CpuLimitSettings)
    containers: list[str] = []


def load_settings() -> Settings:
    with open(SETTINGS_FILE, "r") as f:
        data = yaml.safe_load(f)
        return Settings.model_validate(data)
