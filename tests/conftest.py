import os
import pytest

from sanic_envconfig import EnvConfig


@pytest.fixture()
def config(request):
    class C(EnvConfig):
        ATTRIBUTE_STR: str = 'default_str'
        ATTRIBUTE_INT: int = 1
        ATTRIBUTE_FLOAT: float = 1.5
        ATTRIBUTE_BOOL: bool = True

    return C


@pytest.fixture()
def mock_env(mocker):
    def env(dictionary):
        """ 
        Continence: Allows environment vars to be with a dict without
        Need to unwrap.
        """
        return mocker.patch.dict(in_dict=os.environ, clear=True, **dictionary)
    return env


@pytest.fixture()
def sentinel():
    return type('Sentinel', (), {})()
