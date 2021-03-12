Wraps `ConfigParser` and loads configuration variables from one or more ini files.

# Usage

```python
from configloader import Config

Config.register("path/to/config_a.ini")
Config.register("path/to/config_b.ini")
config = Config.load()
value = config.get("section", "key")
```

`Confg` returns a `ConfigParser`.

Keep in mind that `config_b.ini` overrides variables defined in `config_a.ini` when the section and key name are the
same. 

