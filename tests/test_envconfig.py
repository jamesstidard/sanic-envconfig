import pytest


@pytest.mark.parametrize("attribute, value", [
    ('ATTRIBUTE_STR', 'default_str'),
    ('ATTRIBUTE_INT', 1),
    ('ATTRIBUTE_FLOAT', 1.5),
    ('ATTRIBUTE_BOOL', True),
])
def test_get_attributes(config, attribute, value):
    assert getattr(config, attribute) == value


def test_set_attribute(config, sentinel):
    config.ATTRIBUTE_1 = sentinel
    assert config.ATTRIBUTE_1 == sentinel


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
    mock_env(**{attribute: new_value_in})
    assert getattr(config, attribute) == new_value_out
    assert type(getattr(config, attribute)) == value_type


def test_cant_parse(config, mock_env):
    mock_env(ATTRIBUTE_INT='string')
    with pytest.raises(AttributeError):
        print(config.ATTRIBUTE_INT)
