from .envconfig import EnvConfig


__version__ = "1.3.1"

__all__ = ["__version__", "EnvConfig"]


@EnvConfig.parse(bool)
def parse_bool(value: str) -> bool:
    return value.lower() not in ("0", "false", "n", "no", "off")


@EnvConfig.parse(int)
def parse_int(value: str) -> int:
    return int(value)


@EnvConfig.parse(float)
def parse_float(value: str) -> float:
    return float(value)
