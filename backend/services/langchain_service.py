from typing import List, Tuple
import warnings

from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config.settings import settings
from backend.utils.prompt_templates import (
    file_analysis_prompt,
    readme_generation_prompt,
    tech_detection_prompt,
)

# Suppress only LangChain deprecation noise (not all warnings)
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module="langchain",
)


class LangChainService:
    """
    Service for LangChain operations using HuggingFace
    (LangChain v0.3+ / LCEL-based)
    """

    def __init__(self):
        self.llm = self._initialize_llm()
        self.file_analysis_chain = file_analysis_prompt | self.llm
        self.tech_detection_chain = tech_detection_prompt | self.llm

    # ------------------------------------------------------------------
    # LLM Initialization
    # ------------------------------------------------------------------

    def _initialize_llm(self) -> HuggingFaceEndpoint:
        """Initialize HuggingFace LLM"""
        try:
            llm = HuggingFaceEndpoint(
                repo_id=settings.huggingface_model,
                huggingfacehub_api_token=settings.huggingface_api_token,
                temperature=settings.temperature,
                max_new_tokens=settings.max_tokens,
                top_p=settings.top_p,
                timeout=settings.timeout,
            )
            print(f"HuggingFace LLM initialized: {settings.huggingface_model}")
            return llm
        except Exception as e:
            raise RuntimeError(f"Failed to initialize HuggingFace LLM: {e}")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_response(result) -> str:
        """
        Normalize LangChain responses across string / AIMessage outputs
        """
        if isinstance(result, str):
            return result
        if hasattr(result, "content"):
            return result.content
        return str(result)

    # ------------------------------------------------------------------
    # Core LangChain Operations
    # ------------------------------------------------------------------

    def analyze_file(self, file_name: str, file_content: str) -> str:
        """
        Analyze a single file using LangChain
        """
        try:
            result = self.file_analysis_chain.invoke(
                {
                    "file_name": file_name,
                    "file_content": file_content[:2000],
                }
            )
            return self._normalize_response(result)

        except Exception as e:
            return f"[Analysis failed: {e}]"

    def detect_technologies(self, files_info: str, dependencies: str) -> str:
        """
        Detect technologies used in the project
        """
        try:
            result = self.tech_detection_chain.invoke(
                {
                    "files_info": files_info[:1000],
                    "dependencies": dependencies[:1000],
                }
            )
            return self._normalize_response(result).strip()

        except Exception as e:
            print(f" Technology detection failed: {e}")
            return "Unknown"

    def generate_readme(
        self,
        repo_url: str,
        analysis: str,
        dependencies: str,
        file_structure: str,
        semantic_context: str = "",
    ) -> str:
        """
        Generate README using LangChain + HuggingFace
        """
        try:
            # Render prompt explicitly (safe for non-chat HF models)
            rendered_prompt = readme_generation_prompt.invoke(
                {
                    "repo_url": repo_url,
                    "analysis": analysis[:3000],
                    "dependencies": dependencies[:1000],
                    "file_structure": file_structure[:1000],
                    "semantic_context": semantic_context[:1000],
                }
            ).to_string()

            response = self.llm.invoke(rendered_prompt)
            return self._normalize_response(response)

        except Exception as e:
            raise RuntimeError(f"Failed to generate README: {e}")

    # ------------------------------------------------------------------
    # Document Utilities (RAG-ready)
    # ------------------------------------------------------------------

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into overlapping chunks
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        return splitter.split_documents(documents)

    def create_document(self, content: str, metadata: dict) -> Document:
        """
        Create a LangChain Document
        """
        return Document(page_content=content, metadata=metadata)

    # ------------------------------------------------------------------
    # Batch Operations
    # ------------------------------------------------------------------

    def batch_analyze_files(
        self, files: List[Tuple[str, str]]
    ) -> List[str]:
        """
        Analyze multiple files sequentially
        (easy to parallelize later)
        """
        return [
            self.analyze_file(file_name, file_content)
            for file_name, file_content in files
        ]
