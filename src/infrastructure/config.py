import os

import dotenv

dotenv.load_dotenv()

__all__ = [
    'DatabaseConfig',
]


class DatabaseConfig:
    # Database config
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'postgres')
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'root')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', '')
