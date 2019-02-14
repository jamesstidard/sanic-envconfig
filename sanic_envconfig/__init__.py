import os
import sys

from typing import get_type_hints, Type

__version__ = '1.2.1'


class EnvVar:
    prefix = ''
    parsers = {}

    def __init__(self, default, *, owner=None, name: str=None):
        self.default = default
        self.__set_name__(owner, name)

    def __set_name__(self, owner, name: str):
        if owner:
            self.type = get_type_hints(owner).get(name, type(self.default))
        self.name = f'__{name}'

    def __get__(self, instance, owner):
        cli_name = self.name.replace('_', '-').lower()
        env_name = f'{self.prefix}{self.name[2:]}'

        try:
            index = sys.argv.index(cli_name)
        except ValueError:
            pass
        else:
            # safely overflow argv with % len - to handle options with no value
            index = (index+1) % len(sys.argv)
            value = sys.argv[index]
            return self.__parse(value)

        try:
            value = os.environ[env_name]
        except KeyError:
            pass
        else:
            return self.__parse(value)

        return getattr(instance, self.name, self.default)

    def __parse(self, value):
        if self.type not in self.parsers:
            return value

        try:
            return self.parsers[self.type](value)
        except:
            raise AttributeError(
                f'Could not parse "{value}" of type {type(value)} as '
                f'{self.type} using parser {self.parsers[self.type]}'
            )


class EnvConfigMeta(type):

    def __new__(mcs, name, bases, attrs):
        if '_ENV_PREFIX' in attrs:
            EnvVar.prefix = f'{attrs["_ENV_PREFIX"]}_'

        wrapped = {a: EnvVar(v)
                   for a, v in attrs.items()
                   if mcs._should_wrap(a, v)}

        return super().__new__(mcs, name, bases, {**attrs, **wrapped})

    def __setattr__(self, name, value):
        if name == '_ENV_PREFIX':
            EnvVar.prefix = f'{value}_'

        elif self._should_wrap(name, value):
            value = EnvVar(value, owner=self, name=name)

        super().__setattr__(name, value)

    @staticmethod
    def _should_wrap(name, value):
        return (name.isupper()
            and not name.startswith('_')
            and not isinstance(value, EnvVar))


class EnvConfig(metaclass=EnvConfigMeta):

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


@EnvConfig.parse(bool)
def parse_bool(value: str) -> bool:
    return value.lower() not in (
        '0',
        'false',
        'n',
        'no',
        'off',
    )


@EnvConfig.parse(int)
def parse_int(value: str) -> int:
    return int(value)


@EnvConfig.parse(float)
def parse_float(value: str) -> float:
    return float(value)
