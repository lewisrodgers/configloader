from abc import ABCMeta, abstractmethod

from configloader.exceptions import ConfigNotFound, NoOptionError, MissingOptionsError


class ConfigLoader(metaclass=ABCMeta):
    configs = {}

    def __init__(self):
        self._config_name: str = ""

    @classmethod
    def register(cls, name, path_to_config_file) -> None:
        cls.configs[name] = path_to_config_file

    def load(self, name):
        if name not in self.configs:
            raise ConfigNotFound(name)
        self._config_name = name
        return self.load_config()

    @abstractmethod
    def get(self, *args):
        raise NotImplementedError

    @abstractmethod
    def load_config(self):
        raise NotImplementedError

    def option(self, *args):
        raise NotImplementedError


class Validator(metaclass=ABCMeta):

    def __init__(self, config):
        self._config = config
        self._options = []
        self._options_not_found = []
        self._ok = False

    @property
    def ok(self):
        return self._ok

    @ok.setter
    def ok(self, value):
        self._ok = value

    def register(self, option: str):
        self._options.append(option)

    def validate(self):
        for option in self._options:
            props = option.split(".")
            for prop in props:
                try:
                    self._config[prop]
                except (KeyError, TypeError):
                    self._options_not_found.append(NoOptionError(prop).message)
                else:
                    self._config = self._config[prop]
        if not self._options_not_found:
            self.ok = True

    def raise_for_status(self):
        if self._options_not_found:
            raise MissingOptionsError(" ".join(self._options_not_found))



class ValueGetter(metaclass=ABCMeta):
    @abstractmethod
    def get(self, key):
        raise NotImplementedError

    @abstractmethod
    def value(self):
        raise NotImplementedError
