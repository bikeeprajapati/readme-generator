from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="README Generator API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class RepoRequest(BaseModel):
    repo_url: str

# Response model
class ReadmeResponse(BaseModel):
    readme_content: str
    success: bool
    message: str


@app.get("/")
async def root():
    return {"message": "README Generator API is running"}


@app.post("/generate-readme", response_model=ReadmeResponse)
async def generate_readme(request: RepoRequest):
    """Generate README.md from GitHub repository URL"""
    
    # TODO: Implement your logic here
    # 1. Clone the repository
    # 2. Extract files and information
    # 3. Use LangChain to generate README
    # 4. Return the generated content
    
    try:
        repo_url = request.repo_url
        
        # Your implementation goes here
        readme_content = "# Generated README\n\nYour logic here..."
        
        return ReadmeResponse(
            readme_content=readme_content,
            success=True,
            message="README generated successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)