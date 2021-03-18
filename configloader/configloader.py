from configparser import ConfigParser, ExtendedInterpolation

import toml

from configloader.exceptions import ConfigTomlMalformed, \
    ConfigIniMalformed, NoOptionError
from configloader.interface import ConfigLoader, ValueGetter


class ConfigValueGetter(ValueGetter):
    def __init__(self, values):
        self._values = values
        self._value = None

    def get(self, key):
        if key not in self._values.keys():
            raise NoOptionError(key)
        self._value = self._values[key]
        if isinstance(self._value, dict):
            self._value = ConfigValueGetter(self._value)
        return self.value()

    def value(self):
        return self._value


class INIConfigLoader(ConfigLoader):
    configs = {}

    def __init__(self):
        super().__init__()
        self._config = None
        self._value = None

    def parse_config(self) -> None:
        self._config = ConfigParser(interpolation=ExtendedInterpolation())
        self._config.read(self.configs[self._config_name])

    def set_initial_value(self):
        self._value = ConfigValueGetter(self._config)

    def load_config(self):
        self.parse_config()
        self.set_initial_value()
        return self

    def get(self, key):
        try:
            return self._value.get(key)
        except NoOptionError as e:
            raise ConfigIniMalformed(self._config_name, e)


class TOMLConfigLoader(ConfigLoader):
    configs = {}

    def __init__(self):
        super().__init__()
        self._config = None
        self._value = None

    def load_config(self, name):
        self._config = toml.load(open(self.configs[name]))
        self._value = ConfigValueGetter(self._config)
        return self

    def get(self, key):
        try:
            return self._value.get(key)
        except NoOptionError as e:
            raise ConfigTomlMalformed(self._config_name, e)
