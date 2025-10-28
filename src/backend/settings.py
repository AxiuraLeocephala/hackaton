from typing import Dict
import pathlib
import yaml 

BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent
config_path = BASE_DIR / "config" / "config.yaml"

def get_config():
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config

config = get_config()

CONFIG_SERVER: Dict = config["server"]
CONFIG_LOGGING: Dict = config["logging"]
CONFIG_DATABASE: Dict = config["database"]