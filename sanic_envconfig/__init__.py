import os


class EnvConfigMeta(type):
    __config_meta_parsers = {}

    def __getattribute__(self, name):
        value = super().__getattribute__(name)

        if name in os.environ:
            env_value  = os.environ[name]
            type_hints = self.__annotations__
            value_type = type_hints.get(name, type(value))
            if value_type in self.__config_meta_parsers:
                return self.__config_meta_parsers[value_type](env_value)
            else:
                return env_value
        else:
            return value

    @staticmethod
    def parse(type: type):
        """Create an environ parser from a decorated function.

        :param type: property type to parse
        """

        def decorator(parser):
            EnvConfigMeta.__config_meta_parsers[type] = parser
            return parser

        return decorator


class EnvConfig(metaclass=EnvConfigMeta):
    pass


@EnvConfig.parse(bool)
def parse_bool(value):
    return value.lower() in ('true', 'yes', '1', 'on')


@EnvConfig.parse(int)
def parse_int(value):
    return int(value)


@EnvConfig.parse(float)
def parse_float(value):
    return float(value)
