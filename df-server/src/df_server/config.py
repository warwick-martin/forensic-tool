from pathlib import Path

from pydantic import BaseModel
from ruamel.yaml import YAML
from xdg_base_dirs import xdg_data_home
from xdg_base_dirs import xdg_config_home

def create_global_config_dir():
    """Create the global configuration directory."""
    global_config_dir = xdg_config_home() / 'df'
    global_config_dir.mkdir(parents=True, exist_ok=True)
    return global_config_dir

yaml=YAML(typ='safe')

class Config(BaseModel):
    workspaces_path: Path = ""
    modules_path: Path = ""
    config_file: Path = ""

    def create_default_config(self):
        data_dir = xdg_data_home() / 'df'
        default_config = {
            "workspaces_path": data_dir / 'workspaces',
            "modules_path": data_dir / 'modules'
        }
        with self.config_file.open("w") as f:
            yaml.dump(default_config, f)

    def __init__(self):
        super().__init__()
        config_path: Path = create_global_config_dir()
        self.config_file = config_path / "config.yaml"
        if not self.config_file.exists():
            self.create_default_config()
        with self.config_file.open("r") as f:
            config = yaml.load(f)
            self.workspaces_path = config["workspaces_path"]
            self.modules_path = config["modules_path"]

class ConfigLoader:
    config: Config | None = None

    def __init__(self):
        self.config = Config()


    def __call__(self) -> Config:
        # Redundant check since the class will always be initialised
        if self.config is None:
            self.config = Config()
        return self.config