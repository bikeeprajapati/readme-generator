import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Application settings and configuration using Pydantic v2"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # HuggingFace Settings
    huggingface_api_key: str = ""
    huggingface_model: str = "mistralai/Mistral-7B-Instruct-v0.2"
    
    # Alternative models you can use:
    # "mistralai/Mistral-7B-Instruct-v0.3"
    # "meta-llama/Meta-Llama-3-8B-Instruct"
    # "microsoft/phi-2"
    # "google/flan-t5-xxl"
    # "HuggingFaceH4/zephyr-7b-beta"
    
    # Optional: OpenAI (fallback)
    openai_api_key: Optional[str] = None
    
    # LangChain Settings
    langchain_tracing_v2: bool = False
    langchain_api_key: Optional[str] = None
    langchain_project: str = "readme-generator"
    
    # Repository Settings
    temp_dir: str = "temp"
    max_file_size: int = 5000  # characters
    max_files_to_analyze: int = 10
    
    # Model Settings
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.95
    
    # Performance Settings
    use_cache: bool = True
    timeout: int = 120  # seconds
    
    def validate_settings(self) -> bool:
        """Validate required settings"""
        if not self.huggingface_api_key and not self.openai_api_key:
            raise ValueError(
                "Either HUGGINGFACE_API_KEY or OPENAI_API_KEY must be set in .env file. "
                "Please check your .env file exists and contains: HUGGINGFACE_API_KEY=hf_..."
            )
        return True

# Create global settings instance
settings = Settings()

