import pytest

from sanic_envconfig import EnvVar


@pytest.mark.parametrize("attribute, value", [
    ('ATTRIBUTE_STR', 'default_str'),
    ('ATTRIBUTE_INT', 1),
    ('ATTRIBUTE_FLOAT', 1.5),
    ('ATTRIBUTE_BOOL', True),
])
def test_get_attributes(config, attribute, value):
    assert getattr(config, attribute) == value


def test_set_existing_attribute(config, sentinel):
    config.ATTRIBUTE_STR = sentinel
    assert config.ATTRIBUTE_STR == sentinel


def test_set_existing_attribute_gets_overridden(config, mock_env, sentinel):
    mock_env({'ATTRIBUTE_INT': '1'})
    config.ATTRIBUTE_INT = sentinel
    assert config.ATTRIBUTE_INT == 1


def test_set_new_attribute_gets_overridden(config, mock_env, sentinel):
    mock_env({'ATTRIBUTE_NEW': 'hello attr'})
    config.ATTRIBUTE_NEW = sentinel
    assert config.ATTRIBUTE_NEW == 'hello attr'


def test_no_attribute(config):
    assert not hasattr(config, 'MISSING_ATTRIBUTE')


def test_add_attribute(config, sentinel):
    config.NEW_ATTRIBUTE = sentinel
    assert config.NEW_ATTRIBUTE == sentinel


@pytest.mark.parametrize("attribute, value_type, new_value_in, new_value_out", [
    ("ATTRIBUTE_STR", str, 'new value', 'new value'),
    ("ATTRIBUTE_INT", int, '12345', 12345),
    ("ATTRIBUTE_FLOAT", float, '3.14', 3.14),
    ("ATTRIBUTE_BOOL", bool, 'yes', True),
])
def test_env_override(config, mock_env, attribute, value_type, new_value_in, new_value_out):
    mock_env({attribute: new_value_in})
    assert getattr(config, attribute) == new_value_out
    assert type(getattr(config, attribute)) == value_type


def test_cant_parse(config, mock_env):
    mock_env({'ATTRIBUTE_INT': 'string'})
    with pytest.raises(AttributeError):
        print(config.ATTRIBUTE_INT)


def test_default_not_parsed(config):
    parsers = EnvVar.parsers

    def trap(*_, **__):
        assert False

    EnvVar.parsers = {k: trap for k, v in parsers.items()}

    print(config.ATTRIBUTE_BOOL)

    EnvVar.parsers = parsers


def test_cant_access_undefined_var(config, mock_args, mock_env):
    mock_args('--not-on-config "oh no"')
    mock_env({'NOT_ON_CONFIG': 'oh no'})
    with pytest.raises(AttributeError):
        print(config.NOT_ON_CONFIG)


def test_args_override_env(config, mock_args, mock_env):
    correct, incorrect = 'correct', 'incorrect'
    mock_env({'ATTRIBUTE_STR': incorrect})
    assert config.ATTRIBUTE_STR == incorrect
    mock_args(f'--attribute-str {correct}')
    assert config.ATTRIBUTE_STR == correct


def test_args_quoted(config, mock_args):
    something_in_quotes = 'something in quotes'
    mock_args(f'--attribute-str "{something_in_quotes}"')
    assert config.ATTRIBUTE_STR == something_in_quotes


def test_normal_property_set(config, mock_env, sentinel):
    mock_env({'normal': 'oh no'})
    config.normal = sentinel
    assert config.normal is sentinel


@pytest.mark.parametrize("attribute, default, new", [
    ('ATTRIBUTE_STR', 'default_str', 'new_str'),
    ('ATTRIBUTE_INT', 1, 2),
    ('ATTRIBUTE_FLOAT', 1.5, 5.0),
    ('ATTRIBUTE_BOOL', True, False),
])
def test_get_prefixed_env(prefix_config, attribute, default, new, mock_env):
    assert getattr(prefix_config, attribute) == default
    mock_env({f'PREFIX_{attribute}': str(new)})
    assert getattr(prefix_config, attribute) == new


@pytest.mark.parametrize("attribute, default, new", [
    ('ATTRIBUTE_STR', 'default_str', 'new_str'),
    ('ATTRIBUTE_INT', 1, 2),
    ('ATTRIBUTE_FLOAT', 1.5, 5.0),
    ('ATTRIBUTE_BOOL', True, False),
])
def test_no_prefixed_env_used(prefix_config, attribute, default, new, mock_env):
    assert getattr(prefix_config, attribute) == default
    mock_env({attribute: str(new)})
    assert getattr(prefix_config, attribute) == default
