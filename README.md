# ConfigManager

The `ConfigManager` is a Python utility class for managing multiple YAML configuration files. It allows easy loading, reloading, and retrieval of configuration values by using aliases to reference different files. This is designed to be used as a submodule in larger projects to facilitate structured configuration handling.

## Features

- Load multiple configuration files with aliases.
- Reload configurations on demand.
- Retrieve specific or all keys from a configuration.
- Error handling to ensure robust management of configurations.

## Installation

Clone this repository or add it as a submodule to your project:

```bash
git submodule add <repository_url> configmanager
```

Make sure that `PyYAML` is installed, as it is required for reading YAML files:

```bash
pip install pyyaml
```

## Usage

### Importing ConfigManager

To use `ConfigManager` in your project, import it as follows:

```python
from configmanager import ConfigManager, ConfigError
```

### Initialization

The `ConfigManager` is initialized with a dictionary that maps aliases to file paths:

```python
config_files = {
    "app_config": "config/app_config.yaml",
    "db_config": "config/db_config.yaml"
}
config_manager = ConfigManager(config_files)
```

### Reloading Configurations

To reload all or some of the configurations, use the `reload_configs` method:

```python
# Reload all configurations
config_manager.reload_configs()

# Reload a specific configuration by alias
config_manager.reload_configs("app_config")
```

### Retrieving Configuration Values

To retrieve configuration values, use the `get` method:

```python
# Get the entire configuration for an alias
app_config = config_manager.get(alias="app_config")

# Get a specific key from the configuration
db_host = config_manager.get(keys="host", alias="db_config")

# Get multiple keys from the configuration
db_settings = config_manager.get(keys=["host", "port"], alias="db_config")
```

### Error Handling

`ConfigManager` raises a custom exception called `ConfigError` in case of invalid operations or if any issues occur when loading configurations:

```python
try:
    value = config_manager.get(keys="nonexistent_key", alias="app_config")
except ConfigError as e:
    print(f"Error: {e}")
```

## Example Configuration File

Below is an example of a YAML configuration file (`app_config.yaml`):

```yaml
app_name: MyApp
version: 1.0.0
debug: true
```

This can be accessed as follows:

```python
app_name = config_manager.get(keys="app_name", alias="app_config")
```

## Contributing

Contributions are welcome!

## Limitations

- Currently, only YAML files are supported.
- Configuration files must exist before being loaded, otherwise a `ConfigError` is raised.


If you have any questions or feedback, feel free to reach out!

