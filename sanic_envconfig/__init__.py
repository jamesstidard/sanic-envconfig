import os
import typing


parsers = {}


class EnvConfigMeta(type):

    def __getattribute__(self, name):
        default_value = super().__getattribute__(name)

        if name not in os.environ:
            return default_value
        else:
            env_value = os.environ[name]
            type_hints = typing.get_type_hints(self)
            value_type = type_hints.get(name, type(default_value))

            if value_type not in parsers:
                return env_value
            else:
                try:
                    return parsers[value_type](env_value)
                except Exception:
                    raise AttributeError(
                        f'Could not parse "{env_value}" of type {type(env_value)} '
                        f'as {value_type} using parser {parsers[value_type]}')


class EnvConfig(metaclass=EnvConfigMeta):

    def __getattribute__(self, name):
        default_value = super().__getattribute__(name)

        if name not in os.environ:
            return default_value
        else:
            env_value = os.environ[name]
            type_hints = typing.get_type_hints(self)
            value_type = type_hints.get(name, type(default_value))

            if value_type not in parsers:
                return env_value
            else:
                try:
                    return parsers[value_type](env_value)
                except Exception:
                    raise AttributeError(
                        f'Could not parse "{env_value}" of type {type(env_value)} '
                        f'as {value_type} using parser {parsers[value_type]}')

    @staticmethod
    def parse(type: type):
        """Create an environ parser from a decorated function.

        :param type: property type to parse
        """

        def decorator(parser):
            parsers[type] = parser
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
