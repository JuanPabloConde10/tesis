import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    """Configuración mínima para la aplicación usando variables de entorno."""
    default_provider: str = os.getenv("DEFAULT_PROVIDER", "openai")


# Instancia global
settings = Settings()
