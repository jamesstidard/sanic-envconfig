import os
import sys
import shlex
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
        Convenience: Allows environment vars to be 
        set with a dict without need to unwrap.
        """
        return mocker.patch.dict(in_dict=os.environ, clear=True, **dictionary)
    return env


@pytest.fixture()
def mock_args(mocker):
    def args(string):
        """ 
        Convenience: Allows commandline args to be 
        set with a string.
        """
        argv = ['/mock/tests/conftest.py', *shlex.split(string)]
        return mocker.patch.object(sys, 'argv', new=argv)
    return args


@pytest.fixture()
def sentinel():
    return type('Sentinel', (), {})()
