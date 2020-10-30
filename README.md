# sanic-envconfig
[![Python Versions](https://img.shields.io/pypi/pyversions/sanic-envconfig.svg)](https://pypi.python.org/pypi/sanic-envconfig)
[![PyPI Version](https://img.shields.io/pypi/v/sanic-envconfig.svg)](https://pypi.python.org/pypi/sanic-envconfig)
[![Licence](http://img.shields.io/:license-mit-blue.svg)](https://github.com/jamesstidard/sanic-envconfig/blob/master/LICENCE.txt)
[![Build Status](https://travis-ci.org/jamesstidard/sanic-envconfig.svg?branch=master)](https://travis-ci.org/jamesstidard/sanic-envconfig)
[![Coverage Status](https://coveralls.io/repos/github/jamesstidard/sanic-envconfig/badge.svg)](https://coveralls.io/github/jamesstidard/sanic-envconfig)

This extension helps you bring commandline & environment variables into your Sanic config.

The extension also leverages type hints to correctly cast those variables to the appropriate type. This can also be overridden and extended for your own types.

## How it Works
Define your config class and subclass `sanic_envconfig.EnvConfig`. To not pollute your config, only those variables defined (and in uppercase) in your config class will pulled from your environment or commandline variables.

The values set in your class will be the default values, overridden when there is a environment variable or commandline argument with the same name available. The priority order being: `commandline arguments > enviroment variables > config`. 

Casting of the commandline & environment variables is decided by looking at the type hints declared on config class. If no hint has been declared, the type of the default value will be used. When a default value is also not provided the variable will be returned as whatever type it exists in `os.environ` or `sys.argv` (most certainly a `str`).

This extension takes care of correctly casting the common types `str`, `bool`, `int` and `float`. Though, `sanic_envconfig.EnvConfig` can be extended for custom types. Additionally, the supplied casting can be overridden if desired.

## Just Sanic?
The extension, for the moment, is generic enough where it could be used in another context. Though, future releases may more tightly couple it with Sanic.

## Installation
```bash
$ pip install sanic_envconfig
```

## Example Usage
```bash
DEBUG: false
DB_URL: postgresql://localhost:5433/environ
WORKERS: 4

$ python example.py --db-url "postgresql://localhost:5433/commandline"
```
```python
# example.py
from sanic import Sanic
from sanic_envconfig import EnvConfig


class Config(EnvConfig):
    DEBUG: bool = True
    DB_URL: str = None
    WORKERS: int = 1

config = Config()

app = Sanic(__name__)
app.update_config(Config)

app.config.DEBUG  # False
app.config.DB_URL  # 'postgresql://localhost:5433/commandline'
app.config.WORKERS  # 4
```

## Custom Casting
To override or extend the casting system, `sanic_envconfig.EnvConfig` provides a decorator. The decorator takes the type as a parameter and hands the decorated function any values of that type from the environment variables.
```bash
THEME: blue
```
```python
from enum import Enum
from sanic_envconfig import EnvConfig


class Color(Enum):
    RED = 0
    BLUE = 1

class Config(EnvConfig):
    THEME: Color = None

@Config.parse(Color)
def parse_color(value):
    return Color[value.upper()]

Config.THEME  # Color.BLUE
```
