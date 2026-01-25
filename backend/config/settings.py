from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings (Pydantic v2 compatible)"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------
    # API Settings
    # -------------------------
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True

    # -------------------------
    # HuggingFace Settings
    # -------------------------
    huggingface_api_token: Optional[str] = None
    huggingface_model: str = "mistralai/Mistral-7B-Instruct-v0.2"

    # -------------------------
    # OpenAI fallback (optional)
    # -------------------------
    openai_api_key: Optional[str] = None

    # -------------------------
    # LangChain Settings
    # -------------------------
    langchain_tracing_v2: bool = False
    langchain_api_key: Optional[str] = None
    langchain_project: str = "readme-generator"

    # -------------------------
    # Repository Limits
    # -------------------------
    temp_dir: str = "temp"
    max_file_size: int = 5000
    max_files_to_analyze: int = 10

    # -------------------------
    # Model Parameters
    # -------------------------
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.95   

    # -------------------------
    # Performance
    # -------------------------
    use_cache: bool = True
    timeout: int = 120

    # -------------------------
    # Validation
    # -------------------------
    def validate_settings(self) -> None:
        if not (self.huggingface_api_token or self.openai_api_key):
            raise ValueError(
                "Either HUGGINGFACE_API_TOKEN or OPENAI_API_KEY must be set"
            )


# Global instance
settings = Settings()
settings.validate_settings()
