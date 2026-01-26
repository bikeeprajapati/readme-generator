from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.api.routes import router
from backend.config.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup - Validate settings here instead of on import
    try:
        settings.validate_settings()
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}\n")
        raise
    
    print("\n" + "="*60)
    print("🚀 README Generator API Started!")
    print("="*60)
    print(f"📝 Model: {settings.huggingface_model}")
    print(f"🌐 Host: {settings.api_host}:{settings.api_port}")
    print(f"📚 Docs: http://{settings.api_host}:{settings.api_port}/docs")
    print(f"🔧 Debug Mode: {settings.debug}")
    print("="*60 + "\n")
    
    yield
    
    # Shutdown
    print("\n👋 Shutting down README Generator API...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="README Generator API",
    description="Generate professional README.md files using HuggingFace + LangChain",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )