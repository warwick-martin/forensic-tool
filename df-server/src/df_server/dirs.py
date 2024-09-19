"""Helper functions for working with directories."""

import os
from pathlib import Path
from uuid import UUID
from .config import Config

def contains_file(directory: str, file_name: str) -> bool:
    """Check if a directory contains a file with the specified name."""
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name == file_name:
            return True
    return False

def create_workspaces_dir(config: Config):
    """Create the workspaces directory."""
    path = Path(config.workspaces_path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def create_workspace_dir(config: Config, id: UUID):
    """Create the workspace directory."""
    path = Path(config.workspaces_path) / str(id)
    path.mkdir(parents=True, exist_ok=True)
    return path

def create_evidence_dir(config: Config, workspace_id: UUID):
    """Create the evidence directory."""
    path = Path(config.workspaces_path) / str(workspace_id) / 'evidence'
    path.mkdir(parents=True, exist_ok=True)
    return path

def create_modules_dir(config: Config):
    """Create the module directory."""
    path = Path(config.modules_path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_hierarchical_structure(folder_path: Path):
    folder_structure = {}

    for dirpath, dirnames, filenames in os.walk(folder_path):
        # Get the current directory as a nested structure in the dict
        current_level = folder_structure
        relative_path = os.path.relpath(dirpath, folder_path)  # Get the relative path

        if relative_path != '.':  # Ignore root folder itself
            for part in relative_path.split(os.sep):
                current_level = current_level.setdefault(part, {})

        # Add files in the current directory
        current_level['files'] = filenames

    return folder_structure