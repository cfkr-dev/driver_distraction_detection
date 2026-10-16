import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_FILE)

# Project root
_project_root = os.getenv("PROJECT_ROOT")

if not _project_root:
    raise EnvironmentError(
        f"PROJECT_ROOT is not defined in {ENV_FILE}"
    )

PROJECT_ROOT = Path(_project_root).resolve()

if not PROJECT_ROOT.is_dir():
    raise NotADirectoryError(
        f"PROJECT_ROOT does not exist: {PROJECT_ROOT}"
    )
