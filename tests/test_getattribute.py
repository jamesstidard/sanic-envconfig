

def test_get_attributes(config):
    assert config.ATTRIBUTE_1 == 1
    assert config.ATTRIBUTE_2 == 2
    assert config.ATTRIBUTE_3 == 3


def test_set_attribute(config, sentinel):
    config.ATTRIBUTE_1 = sentinel
    assert config.ATTRIBUTE_1 == sentinel


def test_no_attribute(config):
    assert not hasattr(config, 'MISSING_ATTRIBUTE')


def test_add_attribute(config, sentinel):
    config.NEW_ATTRIBUTE = sentinel
    assert config.NEW_ATTRIBUTE == sentinel


def test_env_override(config, mock_env):
    mock_env(ATTRIBUTE_1='12345')
    assert config.ATTRIBUTE_1 == 12345
