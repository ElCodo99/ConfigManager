# configmanager.py
import yaml
import os

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

class ConfigManager:
    def __init__(self, config_files):
        """
        Initialize the Config object with a mapping of aliases to configuration file paths.
        
        :param config_files: A dictionary mapping aliases to file paths.
        :raises ConfigError: If no configuration files are provided or if the input is not a dictionary.
        """
        if not config_files:
            raise ConfigError("No configuration files provided.")
        if not isinstance(config_files, dict):
            raise ConfigError("config_files must be a dictionary mapping aliases to file paths.")
        
        self.config_files = config_files  # {alias: filename}
        self.configs = {}  # {alias: config_data}

    def _load_config(self, filename, alias):
        """
        Load configuration from a YAML file.

        :param filename: The path to the configuration file.
        :param alias: The alias associated with this configuration.
        :return: The loaded configuration data.
        :raises ConfigError: If the configuration file does not exist.
        """
        if not os.path.exists(filename):
            raise ConfigError(f"Configuration file '{filename}' for alias '{alias}' does not exist.")

        with open(filename, 'r') as file:
            data = yaml.safe_load(file) or {}
            return data

    def reload_configs(self, aliases=None):
        """
        Reload configurations from their respective files.

        :param aliases: A list of aliases to reload. If None, reload all configs.
        :raises ConfigError: If any configuration file fails to load.
        """
        if aliases is None:
            aliases = self.config_files.keys()
        elif isinstance(aliases, str):
            aliases = [aliases]

        for alias in aliases:
            if alias in self.config_files:
                filename = self.config_files[alias]
                self.configs[alias] = self._load_config(filename, alias)
            else:
                raise ConfigError(f"Alias '{alias}' not found in config_files.")

    def get(self, keys=None, alias=None):
        """
        Get the value(s) associated with the key(s) from the specified configuration.

        :param keys: The configuration key, list of keys, or None to get all keys.
        :param alias: The alias of the configuration file.
        :return: The value associated with the key, a dictionary of key-value pairs, or the entire configuration.
        :raises ConfigError: If the alias or key is not found.
        """
        if alias is None:
            if len(self.config_files) == 1:
                alias = next(iter(self.config_files))
            else:
                raise ConfigError("Multiple configurations are loaded. Please specify an alias.")

        if alias not in self.config_files:
            raise ConfigError(f"Alias '{alias}' not found in configuration files.")

        # Reload only the requested alias
        self.reload_configs(alias)

        config = self.configs.get(alias, {})
        if keys is None:
            # Return the entire configuration
            return config
        elif isinstance(keys, str):
            if keys in config:
                return config[keys]
            else:
                raise ConfigError(f"Key '{keys}' not found in configuration '{alias}'.")
        elif isinstance(keys, list):
            result = {}
            for key in keys:
                if key in config:
                    result[key] = config[key]
                else:
                    raise ConfigError(f"Key '{key}' not found in configuration '{alias}'.")
            return result
        else:
            raise ConfigError("keys must be None, a string, or a list of strings.")

