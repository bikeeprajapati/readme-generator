from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
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
        self.file_analysis_chain = self._create_analysis_chain()
        self.tech_detection_chain = self._create_tech_chain()
    
    def _initialize_llm(self):
        """
        Initialize HuggingFace LLM using ChatHuggingFace for better compatibility
        
        Returns:
            LangChain LLM instance
        """
        try:
            # First create the endpoint
            llm = HuggingFaceEndpoint(
                repo_id=settings.huggingface_model,
                huggingfacehub_api_token=settings.huggingface_api_key,
                temperature=settings.temperature,
                max_new_tokens=settings.max_tokens,
                top_p=settings.top_p,
                timeout=settings.timeout,
            )
            
            # Wrap it with ChatHuggingFace for conversational models
            chat_llm = ChatHuggingFace(llm=llm)
            
            print(f"✅ HuggingFace Chat LLM initialized: {settings.huggingface_model}")
            return chat_llm
            
        except Exception as e:
            print(f"⚠️ ChatHuggingFace failed, trying direct endpoint: {str(e)}")
            # Fallback to direct endpoint for non-chat models
            try:
                llm = HuggingFaceEndpoint(
                    repo_id=settings.huggingface_model,
                    huggingfacehub_api_token=settings.huggingface_api_key,
                    temperature=settings.temperature,
                    max_new_tokens=settings.max_tokens,
                    top_p=settings.top_p,
                    timeout=settings.timeout,
                    task="text-generation",
                )
                print(f"✅ HuggingFace Endpoint initialized: {settings.huggingface_model}")
                return llm
            except Exception as e2:
                print(f"❌ Failed to initialize HuggingFace LLM: {str(e2)}")
                raise
    
    def _create_analysis_chain(self):
        """Create file analysis chain"""
        return file_analysis_prompt | self.llm
    
    def _create_tech_chain(self):
        """Create technology detection chain"""
        return tech_detection_prompt | self.llm
    
    def analyze_file(self, file_name: str, file_content: str) -> str:
        """
        Analyze a single file using LangChain (Latest API)
        
        Args:
            file_name: Name of the file
            file_content: Content of the file
            
        Returns:
            Analysis summary
        """
        try:
            # Use the new invoke method (LangChain v0.3+)
            result = self.file_analysis_chain.invoke({
                "file_name": file_name,
                "file_content": file_content[:2000]
            })
            
            # Handle different response types (ChatHuggingFace returns AIMessage)
            if hasattr(result, 'content'):
                return result.content
            elif isinstance(result, str):
                return result
            else:
                return str(result)
                
        except Exception as e:
            print(f"⚠️ File analysis error for {file_name}: {str(e)}")
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
            result = self.tech_detection_chain.invoke({
                "files_info": files_info[:1000],
                "dependencies": dependencies[:1000]
            })
            
            # Handle different response types
            if hasattr(result, 'content'):
                text = result.content.strip()
            elif isinstance(result, str):
                text = result.strip()
            else:
                text = str(result).strip()
            
            # Clean up the response
            if "Technologies:" in text:
                text = text.split("Technologies:")[-1].strip()
            
            return text if text else "Unknown"
                
        except Exception as e:
            print(f"⚠️ Technology detection failed: {str(e)}")
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
        Generate README using LangChain and HuggingFace (Latest API)
        
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
            # Create the prompt
            prompt_text = f"""You are an expert technical writer. Create a professional README.md for this repository.

Repository: {repo_url}

Project Analysis:
{analysis[:2000]}

Dependencies:
{dependencies[:800]}

File Structure:
{file_structure[:800]}

Context:
{semantic_context[:500]}

Generate a complete README.md with these sections:
1. Project Title and Description
2. Features (3-5 bullet points)
3. Technologies Used
4. Installation Instructions
5. Usage Examples
6. Project Structure
7. Contributing
8. License

Use proper Markdown formatting. Be concise but informative."""

            # Invoke the LLM
            if isinstance(self.llm, ChatHuggingFace):
                # For ChatHuggingFace, use messages
                messages = [HumanMessage(content=prompt_text)]
                response = self.llm.invoke(messages)
            else:
                # For regular endpoint
                response = self.llm.invoke(prompt_text)
            
            # Extract content
            if hasattr(response, 'content'):
                return response.content
            elif isinstance(response, str):
                return response
            else:
                return str(response)
            
        except Exception as e:
            print(f"❌ README generation error: {str(e)}")
            raise RuntimeError(f"Failed to generate README: {e}")
    
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