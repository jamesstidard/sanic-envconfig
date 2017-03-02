import os
import typing


class EnvAttribute:
    parsers = {}

    def __init__(self, default=None, name=None, value_type=None):
        self.name = name
        self.type = value_type or type(default)
        self.default = default

    def __get__(self, instance, owner):
        if self.name in os.environ:
            value = os.environ[self.name]
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
            return self.default

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
        self.type = typing.get_type_hints(owner).get(name, self.type)


class EnvConfig:

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        type_hints = typing.get_type_hints(cls)
        for attr in dir(cls):
            if not attr.startswith('_'):
                setattr(cls, attr, EnvAttribute(getattr(cls, attr), attr, type_hints.get(attr, None)))

    @staticmethod
    def parse(type: type):
        """Create an environ parser from a decorated function.

        :param type: property type to parse
        """
        def decorator(parser):
            EnvAttribute.parsers[type] = parser
            return parser

        return decorator


@EnvConfig.parse(bool)
def parse_bool(value):
    return value.lower() in ('true', 'yes', '1', 'on')


@EnvConfig.parse(int)
def parse_int(value):
    return int(value)


@EnvConfig.parse(float)
def parse_float(value):
    return float(value)
