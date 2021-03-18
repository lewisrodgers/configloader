class Error(Exception):
    pass


class ConfigError(Error):
    pass


class NoOptionError(ConfigError):
    def __init__(self, key):
        self.message = f"'{key}' option not found."
        super().__init__(self.message)


class MissingOptionsError(ConfigError):
    def __init__(self, no_option_error):
        self.message = no_option_error
        super().__init__(self.message)


class ConfigMalformed(ConfigError):
    def __init__(self, kind, name, err):
        self.message = f"{kind} configuration for '{name}' is malformed. {err}"
        super().__init__(self.message)


class ConfigIniMalformed(ConfigMalformed):
    def __init__(self, name, err):
        super().__init__("INI", name, err)


class ConfigTomlMalformed(ConfigMalformed):
    def __init__(self, name, err):
        super().__init__("TOML", name, err)


class ConfigNotFound(ConfigError):
    def __init__(self, kind, name):
        self.message = f"{kind} configuration for '{name}' not found."
        super().__init__(self.message)


class ConfigIniNotFound(ConfigNotFound):
    def __init__(self, name):
        super().__init__("INI", name)


class ConfigTomlNotFound(ConfigNotFound):
    def __init__(self, name):
        super().__init__("TOML", name)
