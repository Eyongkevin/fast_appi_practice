import os
from pathlib import Path

from pydantic import BaseSettings

class Settings(BaseSettings):
    """Global application settings"""

    PROJECT_NAME: str =  os.getenv('PROJECT_NAME', 'Sql-app')
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./sql_app.db")
    ROOT_DIR: str = os.getenv('ROOT_DIR', str(Path(__file__).resolve().parent.parent.parent))
    IMAGE_DIR: str = os.getenv('IMAGE_DIR', os.path.join(ROOT_DIR, 'images'))
    MAX_LIMIT: str = os.getenv('MAX_LIMIT', '100')