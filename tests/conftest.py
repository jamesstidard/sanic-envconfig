import os
import pytest

from enum import Enum
from functools import partial

from sanic_envconfig import EnvConfig


class ConfigType(Enum):
    INSTANCE = 0
    CLASS = 1


@pytest.fixture(params=[ConfigType.CLASS, ConfigType.INSTANCE])
def config(request):
    class C(EnvConfig):
        ATTRIBUTE_STR: str = 'default_str'
        ATTRIBUTE_INT: int = 1
        ATTRIBUTE_FLOAT: float = 1.5
        ATTRIBUTE_BOOL: bool = True

    if request.param == ConfigType.CLASS:
        return C
    else:
        return C()


@pytest.fixture()
def mock_env(mocker):
    return partial(mocker.patch.dict, in_dict=os.environ, clear=True)


@pytest.fixture()
def sentinel():
    return object()
