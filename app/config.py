"""OCR Docling API Application Configuration"""

import logging
import os
from typing import Set, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class Environment(Enum):
    """Enum for application environments"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class DatabaseConfig:
    """Database configuration"""

    url: str = "postgresql://csai_user:8akWs89Od5O82wsZfkKzse3c@localhost:5445/csai_db"
    pool_size: int = 10
    max_overflow: int = 20
    echo: bool = False


@dataclass
class ServerConfig:
    """Server configuration"""

    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    reload: bool = True
    log_level: str = "INFO"


@dataclass
class CorsConfig:
    """CORS configuration"""

    origins: List[str] = None

    def __post_init__(self):
        if self.origins is None:
            self.origins = [
                "http://localhost:3000",
                "http://localhost:2137",
                "http://localhost:5173",
                "http://localhost:8080",
            ]


@dataclass
class ApiConfig:
    """API configuration"""

    title: str = "Docling OCR API"
    description: str = "API for OCR processing and language detection using Docling"
    version: str = "1.0.0"


@dataclass
class FileConfig:
    """File configuration"""

    max_size: int = 50 * 1024 * 1024  # 50MB
    processing_timeout: int = 300  # 5 minutes
    allowed_extensions: Set[str] = None

    def __post_init__(self):
        if self.allowed_extensions is None:
            self.allowed_extensions = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"}


@dataclass
class AppConfig:
    """Main application configuration"""

    environment: Environment = Environment.DEVELOPMENT
    database: DatabaseConfig = None
    server: ServerConfig = None
    cors: CorsConfig = None
    api: ApiConfig = None
    file: FileConfig = None

    def __post_init__(self):
        if self.database is None:
            self.database = DatabaseConfig()
        if self.server is None:
            self.server = ServerConfig()
        if self.cors is None:
            self.cors = CorsConfig()
        if self.api is None:
            self.api = ApiConfig()
        if self.file is None:
            self.file = FileConfig()


class ConfigManager:
    """Application configuration manager"""

    def __init__(self):
        self._config = None
        self._load_config()

    def _load_config(self):
        """Loads configuration based on environment"""
        env = os.getenv("ENVIRONMENT", "development").lower()

        if env == "production":
            self._config = self._get_production_config()
        elif env == "staging":
            self._config = self._get_staging_config()
        else:
            self._config = self._get_development_config()

        # Override with environment variables if set
        self._override_with_env()

    def _get_development_config(self) -> AppConfig:
        """Configuration for development environment"""
        return AppConfig(
            environment=Environment.DEVELOPMENT,
            database=DatabaseConfig(
                # Domyślnie używamy SQLite w development, aby nie wymagać lokalnego Postgresa
                url="sqlite:///ocr_documents.db",
                echo=True,  # Enable SQL logging in development
            ),
            server=ServerConfig(
                host="0.0.0.0", port=8000, debug=True, reload=True, log_level="DEBUG"
            ),
            cors=CorsConfig(
                origins=[
                    "http://localhost:3000",
                    "http://localhost:2137",
                    "http://localhost:5173",
                    "http://localhost:8080",
                    "http://127.0.0.1:3000",
                    "http://127.0.0.1:2137",
                ]
            ),
            api=ApiConfig(
                title="Docling OCR API (Development)",
                description="API for OCR processing and language detection using Docling",
                version="1.0.0",
            ),
            file=FileConfig(
                max_size=50 * 1024 * 1024,  # 50MB
                processing_timeout=300,  # 5 minutes
                allowed_extensions={".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"},
            ),
        )

    def _get_staging_config(self) -> AppConfig:
        """Configuration for staging environment"""
        return AppConfig(
            environment=Environment.STAGING,
            database=DatabaseConfig(
                url="postgresql://csai_user:8akWs89Od5O82wsZfkKzse3c@localhost:5445/csai_db",
                echo=False,
            ),
            server=ServerConfig(
                host="0.0.0.0", port=8000, debug=False, reload=False, log_level="INFO"
            ),
            cors=CorsConfig(
                origins=[
                    "https://staging.yourdomain.com",
                    "https://app-staging.yourdomain.com",
                ]
            ),
            api=ApiConfig(
                title="Docling OCR API (Staging)",
                description="API for OCR processing and language detection using Docling",
                version="1.0.0",
            ),
            file=FileConfig(
                max_size=100 * 1024 * 1024,  # 100MB
                processing_timeout=600,  # 10 minutes
                allowed_extensions={".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"},
            ),
        )

    def _get_production_config(self) -> AppConfig:
        """Configuration for production environment"""
        return AppConfig(
            environment=Environment.PRODUCTION,
            database=DatabaseConfig(
                url="postgresql://csai_user:8akWs89Od5O82wsZfkKzse3c@localhost:5445/csai_db",
                echo=False,
            ),
            server=ServerConfig(
                host="0.0.0.0",
                port=8000,
                debug=False,
                reload=False,
                log_level="WARNING",
            ),
            cors=CorsConfig(
                origins=["https://yourdomain.com", "https://app.yourdomain.com"]
            ),
            api=ApiConfig(
                title="Docling OCR API",
                description="API for OCR processing and language detection using Docling",
                version="1.0.0",
            ),
            file=FileConfig(
                max_size=200 * 1024 * 1024,  # 200MB
                processing_timeout=900,  # 15 minutes
                allowed_extensions={".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"},
            ),
        )

    def _override_with_env(self):
        """Overrides configuration with environment variables"""
        # Database config
        if os.getenv("DATABASE_URL"):
            self._config.database.url = os.getenv("DATABASE_URL")
        if os.getenv("DB_POOL_SIZE"):
            self._config.database.pool_size = int(os.getenv("DB_POOL_SIZE"))
        if os.getenv("DB_MAX_OVERFLOW"):
            self._config.database.max_overflow = int(os.getenv("DB_MAX_OVERFLOW"))
        if os.getenv("DB_ECHO"):
            self._config.database.echo = os.getenv("DB_ECHO").lower() == "true"

        # Server config
        if os.getenv("HOST"):
            self._config.server.host = os.getenv("HOST")
        if os.getenv("PORT"):
            self._config.server.port = int(os.getenv("PORT"))
        if os.getenv("DEBUG"):
            self._config.server.debug = os.getenv("DEBUG").lower() == "true"
        if os.getenv("LOG_LEVEL"):
            self._config.server.log_level = os.getenv("LOG_LEVEL")

        # CORS config
        if os.getenv("CORS_ORIGINS"):
            cors_origins = os.getenv("CORS_ORIGINS")
            self._config.cors.origins = [
                origin.strip() for origin in cors_origins.split(",")
            ]

        # API config
        if os.getenv("API_TITLE"):
            self._config.api.title = os.getenv("API_TITLE")
        if os.getenv("API_DESCRIPTION"):
            self._config.api.description = os.getenv("API_DESCRIPTION")
        if os.getenv("API_VERSION"):
            self._config.api.version = os.getenv("API_VERSION")

        # File config
        if os.getenv("MAX_FILE_SIZE"):
            self._config.file.max_size = int(os.getenv("MAX_FILE_SIZE"))
        if os.getenv("PROCESSING_TIMEOUT"):
            self._config.file.processing_timeout = int(os.getenv("PROCESSING_TIMEOUT"))

    @property
    def config(self) -> AppConfig:
        """Returns current configuration"""
        return self._config

    def get_cors_origins(self) -> List[str]:
        """Returns list of allowed CORS origins"""
        return self._config.cors.origins

    def get_allowed_extensions(self) -> Set[str]:
        """Returns allowed file extensions"""
        return self._config.file.allowed_extensions

    def is_development(self) -> bool:
        """Checks if application is in development mode"""
        return self._config.environment == Environment.DEVELOPMENT

    def is_production(self) -> bool:
        """Checks if application is in production mode"""
        return self._config.environment == Environment.PRODUCTION


# Initialize configuration manager
config_manager = ConfigManager()

# Logging settings
logging.basicConfig(level=getattr(logging, config_manager.config.server.log_level))
logger = logging.getLogger(__name__)

# Language code mapping
LANGUAGE_NAMES = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "et": "Estonian",
    "fa": "Persian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "kn": "Kannada",
    "ko": "Korean",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pa": "Punjabi",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "sq": "Albanian",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)",
}

# Backward compatibility
CORS_ORIGINS = config_manager.get_cors_origins()
ALLOWED_EXTENSIONS = config_manager.get_allowed_extensions()
