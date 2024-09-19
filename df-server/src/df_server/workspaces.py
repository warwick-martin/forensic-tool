from pathlib import Path
from typing import List, Optional
from uuid import UUID, uuid4
import os

from .modules import Module
from ruamel.yaml import YAML

from .dirs import contains_file, create_evidence_dir, create_workspace_dir

from .config import Config

class WorkspaceConfig:
    """A workspace configuration file."""
    _name: str = "" # Name of the workspace
    _modules: List[str] = [] # List of module names in the workspace

    # Load from disk if it exists, otherwise create it
    def __init__(self, workspace_dir: Path, name: Optional[str] = None):
        yaml=YAML(typ='safe')
        config_file = workspace_dir / Path("workspace.yaml")

        if not config_file.exists():
            default_config = {
                "name": name or "project",
                "modules": []
            }
            with config_file.open("w") as f:
                yaml.dump(default_config, f)

        with config_file.open("r") as f:
            config = yaml.load(f)
            self._name = config["name"]
            self._modules = config["modules"]

    # Get or set the name of the workspace
    def name(self, name: Optional[str] = None) -> str:
        if name is not None:
            # Set the name
            self._name = name
            self.commit()
            pass
        # Get the name
        return self._name

    def commit(self):
        pass


def is_valid_uuid(uuid_string: str) -> bool:
    """Check if a string is a valid UUID."""
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False

class Workspace:
    # The workspace config is god. Minimise data stored in the workspace object itself.
    id: UUID = uuid4() # Throwaway ID

    @staticmethod
    def list(config: Config) -> List[UUID]:
        """List all workspaces in the workspaces folder."""
        workspaces = []
        for entry in os.scandir(config.workspaces_path):
            if entry.is_dir() and is_valid_uuid(entry.name) and contains_file(entry.path, "workspace.yaml"):
                workspaces.append(UUID(entry.name))        
        return workspaces
    
    def _create_workspace(self, config: Config, id: UUID):
        """Create a new workspace."""
        create_workspace_dir(config, id)
        create_evidence_dir(config, id)

    def __init__(self, config: Config, id: UUID = uuid4(), name: Optional[str] = None):
        """Create workspace instance. Optionally load from existing."""
        known_workspaces: List[UUID] = Workspace.list(config)

        if id not in known_workspaces:
            self._create_workspace(config, id)

        self.id = id
        self.workspace_config = WorkspaceConfig(config.workspaces_path / Path(str(id)), name)

    def name(self, name: Optional[str] = None) -> str:
        if name is not None:
            # Set the name
            pass
        # Get the name
        pass

    def delete(self):
        pass
