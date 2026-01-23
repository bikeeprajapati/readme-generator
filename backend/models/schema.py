from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List


class RepoRequest(BaseModel):
    """Request model for README generation"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "repo_url": "https://github.com/username/repository"
            }
        }
    )

    repo_url: str = Field(..., description="GitHub repository URL")


class ReadmeResponse(BaseModel):
    """Response model for README generation"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "readme_content": "# Project Title\n\n...",
                "success": True,
                "message": "README generated successfully",
                "metadata": {
                    "files_analyzed": 5,
                    "technologies_detected": ["Python", "JavaScript"]
                }
            }
        }
    )

    readme_content: str = Field(..., description="Generated README content")
    success: bool = Field(..., description="Success status")
    message: str = Field(..., description="Status message")
    metadata: Optional[Dict[str, object]] = Field(
        None, description="Additional metadata"
    )


class HealthResponse(BaseModel):
    """Health check response"""

    status: str = Field(..., description="Service health status")
    langchain_enabled: bool = Field(..., description="LangChain availability")
    model_provider: str = Field(..., description="LLM provider")
