from abc import ABCMeta, abstractmethod
from configparser import ConfigParser, ExtendedInterpolation, NoOptionError, NoSectionError

import toml


class ConfigurationError(Exception):
    pass


class ConfigLoader(metaclass=ABCMeta):
    configs = {}

    @classmethod
    def register(cls, name, path_to_config_file) -> None:
        cls.configs[name] = path_to_config_file

    def load(self, name):
        if name not in self.configs:
            raise ConfigurationError(f"Configuration file for '{name}' not found.")
        self._config_name = name
        return self.load_config(name)

    def get(self, *args):
        try:
            return self.option(*args)
        except (NoOptionError, NoSectionError) as e:
            raise ConfigurationError(f"Configuration INI for '{self._config_name}' is malformed. {e}")

    # def _option(self, *args):
    #     value = self.option(*args)
    #     if value:
    #         return value
    #     raise ConfigurationError(f"")

    @abstractmethod
    def load_config(self, name):
        raise NotImplementedError

    @abstractmethod
    def option(self, *args):
        raise NotImplementedError


class TOMLoptions:
    def __init__(self, options: dict):
        self._options = options
        self._value = None

    def get(self, option):
        if option not in self._options.keys():
            raise ConfigurationError
        self._value = self._options.get(option)
        if isinstance(self._value, dict):
            self._value = TOMLoptions(self._value)
        return self.value()

    def value(self):
        return self._value


class INIoptions:
    def __init__(self, config):
        self._config = config
        self._section = None
        self._option = None

    def set_section(self, section):
        self._section = section

    def set_option(self, option):
        self._option = option

    def get(self, key):
        if not self._section:
            self.set_section(key)
        else:
            self.set_option(key)
            return self.value()
        return self

    def value(self):
        value = self._config.get(self._section, self._option)
        self._section = None
        self._option = None
        return value


class INIConfigLoader(ConfigLoader):
    configs = {}

    def __init__(self):
        self._config = None
        self._section = None

    def load_config(self, name):
        self._config = ConfigParser(interpolation=ExtendedInterpolation())
        self._config.read(self.configs[name])
        self._option = INIoptions(self._config)
        return self

    def option(self, option):
        return self._option.get(option)

    def section(self, section):
        self._section = section
        return self


class TOMLConfigLoader(ConfigLoader):
    configs = {}

    def __init__(self):
        self._config = None
        self._option = None

    def load_config(self, name):
        self._config = toml.load(open(self.configs[name]))
        self._option = TOMLoptions(self._config)
        return self

    def option(self, option):
        return self._option.get(option)
