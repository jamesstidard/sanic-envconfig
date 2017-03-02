import os
from typing import get_type_hints


class EnvVar:
    parsers = {}

    def __init__(self, default, *, owner=None, name=None):
        self.default = default
        self.__set_name__(owner, name)

    def __set_name__(self, owner, name):
        if owner:
            self.type = get_type_hints(owner).get(name, type(self.default))
        self.name = f'__{name}'

    def __get__(self, instance, owner):
        if self.name[2:] in os.environ:
            value = os.environ[self.name[2:]]
            if self.type in self.parsers:
                try:
                    return self.parsers[self.type](value)
                except:
                    raise AttributeError(
                        f'Could not parse "{value}" of type {type(value)} as '
                        f'{self.type} using parser {self.parsers[self.type]}')
            else:
                return value
        else:
            return getattr(instance, self.name, self.default)


class EnvConfigMeta(type):

    def __new__(mcs, name, bases, attrs):
        wrapped = {a: EnvVar(v) for a, v in attrs.items()
                   if not a.startswith('_')
                   and not a == 'parse'}
        return super().__new__(mcs, name, bases, {**attrs, **wrapped})

    def __setattr__(self, name, value):
        value = EnvVar(value, owner=self, name=name)
        super().__setattr__(name, value)


class EnvConfig(metaclass=EnvConfigMeta):

    @staticmethod
    def parse(type: type):
        """
        Register an environ parser for a attribute type.
    
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
    return value.lower() in ('true', 'yes', '1', 'on')


@EnvConfig.parse(int)
def parse_int(value: str) -> int:
    return int(value)


@EnvConfig.parse(float)
def parse_float(value: str) -> float:
    return float(value)
