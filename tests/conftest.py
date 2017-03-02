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
        ATTRIBUTE_1: int = 1
        ATTRIBUTE_2: int = 2
        ATTRIBUTE_3: int = 3

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
