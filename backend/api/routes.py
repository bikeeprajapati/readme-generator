import logging
from fastapi import APIRouter, HTTPException

from backend.models.schema import RepoRequest, ReadmeResponse, HealthResponse
from backend.services.repository_service import RepositoryService
from backend.services.analysis_service import AnalysisService
from backend.services.langchain_service import LangChainService
from backend.config.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
repo_service = RepositoryService()
analysis_service = AnalysisService()
langchain_service = LangChainService()


@router.get("/", tags=["Root"])
async def root():
    return {
        "message": "README Generator API with HuggingFace & LangChain",
        "version": "1.0.0",
        "model": settings.huggingface_model,
    }


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    return HealthResponse(
        status="healthy",
        langchain_enabled=True,
        model_provider="HuggingFace",
    )


@router.post("/generate-readme", response_model=ReadmeResponse, tags=["README"])
async def generate_readme(request: RepoRequest):
    repo_path = None

    try:
        if not repo_service.validate_github_url(request.repo_url):
            raise HTTPException(
                status_code=400,
                detail="Invalid GitHub URL.",
            )

        logger.info(f"Processing repository: {request.repo_url}")

        # Step 1: Clone
        repo_path = repo_service.clone_repository(request.repo_url)

        # Step 2: Analyze
        analysis_results = analysis_service.analyze_repository(repo_path)

        # Step 3: Generate README
        readme_content = langchain_service.generate_readme(
            repo_url=request.repo_url,
            analysis=analysis_results["file_analyses"],
            dependencies=analysis_results["dependencies"],
            file_structure=analysis_results["file_structure"],
            semantic_context=analysis_results.get("semantic_context", ""),
        )

        metadata = {
            "files_analyzed": analysis_results["files_analyzed_count"],
            "primary_language": analysis_results["primary_language"],
            "technologies_detected": analysis_results["technologies"].split(",")[:5],
            "model_used": settings.huggingface_model,
        }

        return ReadmeResponse(
            readme_content=readme_content,
            success=True,
            message="README generated successfully!",
            metadata=metadata,
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("README generation failed")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating README: {str(e)}",
        )

    finally:
        if repo_path:
            repo_service.cleanup_repository(repo_path)


@router.get("/models", tags=["Info"])
async def get_model_info():
    return {
        "provider": "HuggingFace",
        "model": settings.huggingface_model,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
    }
