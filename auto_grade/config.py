from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml


@dataclass
class Config:
    """Configuration instance."""

    # Login details.
    username: str = ""
    password: str = ""

    # Class config.
    groups: List[str] = field(default_factory=list)

    # Misc.
    debug: bool = False

    def load_from_file(self, fpath: str) -> None:
        config_file = Path(fpath)
        config_data = yaml.safe_load(config_file.read_text())

        self.username = config_data["username"]
        self.password = config_data["password"]
        self.groups = config_data["groups"]
        self.debug = config_data["debug"]


config = Config()
