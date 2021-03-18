import pytest

from configloader.exceptions import MissingOptionsError
from configloader.interface import Validator


@pytest.fixture
def config():
    return {
        "foo": {
            "bar": "foobar",
            "baz": {
                "lorem": "hello",
                "ipsum": "world"
            }
        }
    }


@pytest.mark.parametrize("options", [("foo", "foo.bar")])
def test_should_register_options_to_validate(config, options):
    validator = Validator(config)

    for option in options:
        validator.register(option)

    assert len(validator._options) == len(options)


@pytest.mark.parametrize("option, ok", [
    ("foo", True),
    ("foo.bar", True),
    ("fizz", False),
    ("fizz.buzz", False)
])
def test_should_validate_option(config, option, ok):
    validator = Validator(config)
    validator.register(option)

    validator.validate()

    assert validator.ok is ok


@pytest.mark.parametrize("option", ["fizz"])
def test_should_raise_error_for_missing_option(config, option):
    validator = Validator(config)
    validator.register(option)

    validator.validate()
    with pytest.raises(MissingOptionsError) as excinfo:
        validator.raise_for_status()

    assert "fizz" in str(excinfo.value)


@pytest.mark.parametrize("option", ["fizz.buzz"])
def test_should_raise_error_for_missing_nested_options(config, option):
    validator = Validator(config)
    validator.register(option)

    validator.validate()
    with pytest.raises(MissingOptionsError) as excinfo:
        validator.raise_for_status()

    assert "fizz" in str(excinfo.value)
    assert "buzz" in str(excinfo.value)
