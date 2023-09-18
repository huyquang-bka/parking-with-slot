from dataclasses import dataclass
import yaml


@dataclass
class MainConfig:
    weight_path: str = None

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f, Loader=yaml.FullLoader)
        for key, value in config.items():
            setattr(self, key, value)
