import os
import sys

from typing import get_type_hints, Type

from .utils import load_flat_json


class EnvVar:
    prefix = ""
    config = {}
    parsers = {}

    def __init__(self, default, *, owner=None, name: str = None):
        self.default = default
        self.__set_name__(owner, name)

    def __set_name__(self, owner, name: str):
        if owner:
            self.type = get_type_hints(owner).get(name, type(self.default))
        self.name = f"__{name}"

    def __get__(self, instance, owner):
        cli_name = self.name.replace("_", "-").lower()
        env_name = f"{self.prefix}{self.name[2:]}"
        cfg_name = self.name[2:].lower()

        try:
            index = sys.argv.index(cli_name)
        except ValueError:
            pass
        else:
            # safely overflow argv with % len - to handle options with no value
            index = (index + 1) % len(sys.argv)
            value = sys.argv[index]
            return self.__parse(value)

        try:
            value = os.environ[env_name]
        except KeyError:
            pass
        else:
            return self.__parse(value)

        try:
            value = self.config[cfg_name]
        except KeyError:
            pass
        else:
            return self.__parse(value)

        return getattr(instance, self.name, self.default)

    def __parse(self, value):
        if self.type not in self.parsers:
            return value

        if isinstance(value, self.type):
            return value

        try:
            return self.parsers[self.type](value)
        except:
            raise AttributeError(
                f'Could not parse "{value}" of type {type(value)} as '
                f"{self.type} using parser {self.parsers[self.type]}"
            )


class EnvConfigMeta(type):
    def __new__(mcs, name, bases, attrs):
        if "_ENV_PREFIX" in attrs:
            EnvVar.prefix = f'{attrs["_ENV_PREFIX"]}_'

        if "_CONFIG_PATH" in attrs and os.path.isfile(attrs["_CONFIG_PATH"]):
            EnvVar.config = load_flat_json(attrs["_CONFIG_PATH"])

        wrapped = {a: EnvVar(v) for a, v in attrs.items() if mcs._should_wrap(a, v)}

        return super().__new__(mcs, name, bases, {**attrs, **wrapped})

    def __setattr__(self, name, value):
        if name == "_ENV_PREFIX":
            EnvVar.prefix = f"{value}_"

        if name == "_CONFIG_PATH" and os.path.isfile(value):
            EnvVar.config = load_flat_json(value)

        elif self._should_wrap(name, value):
            value = EnvVar(value, owner=self, name=name)

        super().__setattr__(name, value)

    @staticmethod
    def _should_wrap(name, value):
        return (
            name.isupper()
            and not name.startswith("_")
            and not isinstance(value, EnvVar)
        )


class EnvConfig(metaclass=EnvConfigMeta):

    def __init__(self):
        # freeze
        self.__dict__.update(
            {k: getattr(self.__class__, k) for k in vars(self.__class__) if k.isupper()}
        )

    @staticmethod
    def parse(type: Type):
        """
        Register a parser for a attribute type.

        Parsers will be used to parse `str` type objects from either
        the commandline arguments or environment variables.

        Args:
            type: the type the decorated function will be responsible
                for parsing a environment variable to.
        """

        def decorator(parser):
            EnvVar.parsers[type] = parser
            return parser

        return decorator
