from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from backend.config.settings import settings

# Validate settings on startup
settings.validate()

# Initialize FastAPI app
app = FastAPI(
    title="README Generator API",
    description="Generate professional README.md files using HuggingFace + LangChain",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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

# Startup event
@app.on_event("startup")
async def startup_event():
    """Print startup information"""
    print("\n" + "="*60)
    print("🚀 README Generator API Started!")
    print("="*60)
    print(f"📝 Model: {settings.HUGGINGFACE_MODEL}")
    print(f"🌐 Host: {settings.API_HOST}:{settings.API_PORT}")
    print(f"📚 Docs: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    print("="*60 + "\n")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("\n👋 Shutting down README Generator API...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )