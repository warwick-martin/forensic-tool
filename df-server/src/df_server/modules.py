import importlib
import os
import sys
from pathlib import Path
from typing import List
from df_modules import IngestModule, AnalysisModule, ReportModule
import pprint

from .config import Config
from .df_logging import logger

class Module:
    name: str = ""
    module_type: str = ""
    module: IngestModule | AnalysisModule | ReportModule

    def __init__(self, name: str, module_type: str, module: IngestModule | AnalysisModule | ReportModule):
        self.name = name
        self.module_type = module_type
        self.module = module
        pass



def get_modules(config: Config):
    modules_path = os.path.abspath(config.modules_path)
    sys.path.append(str(modules_path))
    modules: List[Module] = []

    for folder_name in os.listdir(modules_path):
        folder_path = os.path.join(modules_path, folder_name)

        max_depth = 2

        # Walk the directory and go up to a specified depth
        for root, dirs, files in os.walk(folder_path):
            # Calculate the current depth based on the directory structure
            current_depth = root[len(folder_path):].count(os.sep)

            # Only process directories up to the max_depth
            if current_depth <= max_depth:
                if '__init__.py' in files:
                    # Extract the relative path from the directory_path
                    relative_path = os.path.relpath(root, folder_path)
                    # Create a valid module name by converting path to dot notation
                    module_name = relative_path.replace(os.sep, '.')

                    # Construct the full path to the __init__.py file
                    init_file_path = os.path.join(root, '__init__.py')

                    # Load the module using importlib
                    spec = importlib.util.spec_from_file_location(module_name, init_file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for t in ["IngestModule", "AnalysisModule", "ReportModule"]:
                        if hasattr(module, t):
                            module_cls = Module(module_name, t, module)
                            # Add the module to sys.modules
                            # sys.modules[module_name] = module
                            modules.append(module_cls)
                            break

    return modules
