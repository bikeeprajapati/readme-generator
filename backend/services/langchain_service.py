from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from huggingface_hub import InferenceClient
from typing import List, Optional
import warnings

from backend.config.settings import settings
from backend.utils.prompt_templates import (
    file_analysis_prompt,
    readme_generation_prompt,
    tech_detection_prompt
)

# Suppress warnings
warnings.filterwarnings('ignore')

class LangChainService:
    """Service for LangChain operations using HuggingFace (Latest Version)"""
    
    def __init__(self):
        """Initialize LangChain service with HuggingFace model"""
        self.llm = self._initialize_llm()
        self.client = InferenceClient(token=settings.huggingface_api_key)
        self.file_analysis_chain = self._create_analysis_chain()
        self.tech_detection_chain = self._create_tech_chain()
    
    def _initialize_llm(self):
        """
        Initialize HuggingFace LLM - simplified version
        
        Returns:
            LangChain LLM instance
        """
        try:
            # Use a model that works well with the inference API
            llm = HuggingFaceEndpoint(
                repo_id=settings.huggingface_model,
                huggingfacehub_api_token=settings.huggingface_api_key,
                temperature=settings.temperature,
                max_new_tokens=settings.max_tokens,
                task="text2text-generation",  # Explicitly set task for FLAN-T5
            )
            
            print(f" HuggingFace LLM initialized: {settings.huggingface_model}")
            return llm
            
        except Exception as e:
            print(f" Failed to initialize HuggingFace LLM: {str(e)}")
            print(f" Tip: Make sure your API token is valid and the model is accessible")
            raise
    
    def _create_analysis_chain(self):
        """Create file analysis chain"""
        return file_analysis_prompt | self.llm
    
    def _create_tech_chain(self):
        """Create technology detection chain"""
        return tech_detection_prompt | self.llm
    
    def _call_inference_api(self, prompt: str, max_new_tokens: int = 500) -> str:
        """
        Direct call to HuggingFace Inference API as fallback
        
        Args:
            prompt: Input prompt
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            response = self.client.text_generation(
                prompt,
                model=settings.huggingface_model,
                max_new_tokens=max_new_tokens,
                temperature=settings.temperature,
            )
            return response
        except Exception as e:
            print(f" Inference API error: {str(e)}")
            return ""
    
    def analyze_file(self, file_name: str, file_content: str) -> str:
        """
        Analyze a single file using HuggingFace Inference API
        
        Args:
            file_name: Name of the file
            file_content: Content of the file
            
        Returns:
            Analysis summary
        """
        try:
            prompt = f"Analyze this code file and provide a brief summary (2-3 sentences):\n\nFile: {file_name}\n\n{file_content[:1500]}\n\nSummary:"
            
            result = self._call_inference_api(prompt, max_new_tokens=200)
            
            return result if result else f"[Analysis skipped - {file_name}]"
                
        except Exception as e:
            print(f" File analysis error for {file_name}: {str(e)}")
            return f"[Analysis skipped - {file_name}]"
    
    def detect_technologies(self, files_info: str, dependencies: str) -> str:
        """
        Detect technologies used in the project
        
        Args:
            files_info: Information about files
            dependencies: Dependency information
            
        Returns:
            Comma-separated list of technologies
        """
        try:
            prompt = f"List all technologies and frameworks used in this project:\n\n{dependencies[:800]}\n\nTechnologies (comma-separated):"
            
            result = self._call_inference_api(prompt, max_new_tokens=100)
            
            return result.strip() if result else "Unknown"
                
        except Exception as e:
            print(f" Technology detection failed: {str(e)}")
            return "Unknown"
    
    def generate_readme(
        self,
        repo_url: str,
        analysis: str,
        dependencies: str,
        file_structure: str,
        semantic_context: str = ""
    ) -> str:
        """
        Generate README using HuggingFace Inference API
        
        Args:
            repo_url: Repository URL
            analysis: File analysis results
            dependencies: Dependencies information
            file_structure: Project structure
            semantic_context: Additional semantic context
            
        Returns:
            Generated README content
        """
        try:
            # Create a concise prompt for FLAN-T5
            prompt = f"""Create a professional README.md for this GitHub repository:

Repository: {repo_url}

Dependencies:
{dependencies[:600]}

Files:
{file_structure[:400]}

Generate a README with:
1. Project title and description
2. Key features (3 points)
3. Technologies used
4. Installation steps
5. Basic usage

README:"""

            # Use longer token limit for README generation
            result = self._call_inference_api(prompt, max_new_tokens=1500)
            
            if not result or len(result) < 50:
                # Fallback: Create a basic README from available info
                return self._create_basic_readme(repo_url, dependencies, file_structure)
            
            return result
            
        except Exception as e:
            print(f"README generation error: {str(e)}")
            # Return fallback README
            return self._create_basic_readme(repo_url, dependencies, file_structure)
    
    def _create_basic_readme(self, repo_url: str, dependencies: str, file_structure: str) -> str:
        """Create a basic README as fallback with improved intelligence"""
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        
        # Detect project type from dependencies
        project_type = "Application"
        tech_stack = []
        install_cmd = "pip install -r requirements.txt"
        run_cmd = "python main.py"
        
        deps_lower = dependencies.lower()
        
        if "fastapi" in deps_lower or "flask" in deps_lower or "django" in deps_lower:
            project_type = "Web API"
            if "fastapi" in deps_lower:
                tech_stack.append("FastAPI")
                run_cmd = "uvicorn app.main:app --reload"
            elif "flask" in deps_lower:
                tech_stack.append("Flask")
                run_cmd = "flask run"
            elif "django" in deps_lower:
                tech_stack.append("Django")
                run_cmd = "python manage.py runserver"
        
        if "streamlit" in deps_lower:
            tech_stack.append("Streamlit")
            project_type = "Data Application"
        
        if "machine learning" in deps_lower or "scikit-learn" in deps_lower or "tensorflow" in deps_lower or "torch" in deps_lower:
            project_type = "Machine Learning Project"
            if "scikit-learn" in deps_lower:
                tech_stack.append("Scikit-learn")
            if "tensorflow" in deps_lower:
                tech_stack.append("TensorFlow")
            if "torch" in deps_lower or "pytorch" in deps_lower:
                tech_stack.append("PyTorch")
        
        if "react" in deps_lower or "vue" in deps_lower or "angular" in deps_lower:
            project_type = "Frontend Application"
            install_cmd = "npm install"
            run_cmd = "npm start"
            if "react" in deps_lower:
                tech_stack.append("React")
            elif "vue" in deps_lower:
                tech_stack.append("Vue.js")
            elif "angular" in deps_lower:
                tech_stack.append("Angular")
        
        if "docker" in file_structure.lower():
            tech_stack.append("Docker")
        
        # Detect language
        language = "Python" if "requirements.txt" in file_structure else "JavaScript" if "package.json" in file_structure else "Unknown"
        
        if language == "Python":
            tech_stack.insert(0, "Python")
        elif language == "JavaScript":
            tech_stack.insert(0, "JavaScript")
        
        tech_stack_str = ", ".join(tech_stack) if tech_stack else "See dependencies below"
        
        return f"""# {repo_name.replace('-', ' ').title()}

## 📋 Description

A {project_type.lower()} built with modern technologies. This repository contains the source code and configuration files for {repo_name}.

## ✨ Features

- 🚀 Modern architecture and clean code structure
- 📦 Well-organized project layout
- 🔧 Easy to set up and configure
- 📝 Comprehensive documentation
- 🧪 Ready for development and testing

## 🛠️ Technologies Used

**Core Stack:** {tech_stack_str}

**Dependencies:**
{dependencies[:400]}

## 📦 Installation

### Prerequisites
- {language} installed on your system
- Git for version control
{'- Docker (optional, for containerized deployment)' if 'docker' in file_structure.lower() else ''}

### Setup Steps

```bash
# 1. Clone the repository
git clone {repo_url}

# 2. Navigate to the project directory
cd {repo_name}

# 3. Install dependencies
{install_cmd}
```

{'### Using Docker\n\n```bash\n# Build the Docker image\ndocker build -t ' + repo_name + ' .\n\n# Run the container\ndocker run -p 8000:8000 ' + repo_name + '\n```' if 'dockerfile' in file_structure.lower() else ''}

## 🚀 Usage

```bash
# Run the application
{run_cmd}
```

The application will be available at `http://localhost:8000` (or the configured port).

## 📁 Project Structure

```
{file_structure[:600]}
```

## 🧪 Testing

```bash
# Run tests
{'pytest' if language == 'Python' else 'npm test'}
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Repository:** [{repo_name}]({repo_url})

## 🙏 Acknowledgments

- Thanks to all contributors
- Built with modern tools and best practices
- Open source community support

---

⭐ **Star this repository if you find it helpful!**
"""
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks using RecursiveCharacterTextSplitter
        
        Args:
            documents: List of LangChain Document objects
            
        Returns:
            List of split documents
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        
        return text_splitter.split_documents(documents)
    
    def create_document(self, content: str, metadata: dict) -> Document:
        """
        Create a LangChain Document
        
        Args:
            content: Document content
            metadata: Document metadata
            
        Returns:
            LangChain Document object
        """
        return Document(page_content=content, metadata=metadata)
    
    def batch_analyze_files(self, files: List[tuple]) -> List[str]:
        """
        Batch analyze multiple files efficiently
        
        Args:
            files: List of (file_name, file_content) tuples
            
        Returns:
            List of analysis results
        """
        results = []
        for file_name, file_content in files:
            analysis = self.analyze_file(file_name, file_content)
            results.append(analysis)
        return results