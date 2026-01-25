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

warnings.filterwarnings("ignore", category=DeprecationWarning)


class LangChainService:
    """LangChain service using HuggingFace Router (stable)"""

    def __init__(self):
        self.llm = self._init_llm()
        self.file_analysis_chain = file_analysis_prompt | self.llm
        self.tech_detection_chain = tech_detection_prompt | self.llm

    # --------------------------------------------------
    # LLM (CORRECT + STABLE)
    # --------------------------------------------------

    def _init_llm(self) -> HuggingFaceEndpoint:
        try:
            llm = HuggingFaceEndpoint(
                repo_id=settings.huggingface_model,
                huggingfacehub_api_token=settings.huggingface_api_token,
                temperature=settings.temperature,
                max_new_tokens=settings.max_tokens,
                top_p=settings.top_p,
                timeout=settings.timeout,
            )

            print(f"✅ HuggingFace Router LLM ready: {settings.huggingface_model}")
            return llm

        except Exception as e:
            raise RuntimeError(f"Failed to initialize HuggingFace LLM: {e}")

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _normalize(result) -> str:
        if isinstance(result, str):
            return result
        if hasattr(result, "content"):
            return result.content
        return str(result)

    # --------------------------------------------------
    # Core Operations
    # --------------------------------------------------

    def analyze_file(self, file_name: str, file_content: str) -> str:
        try:
            result = self.file_analysis_chain.invoke(
                {
                    "file_name": file_name,
                    "file_content": file_content[:2000],
                }
            )
            return self._normalize(result)
        except Exception as e:
            return f"[Analysis failed: {e}]"

    def detect_technologies(self, files_info: str, dependencies: str) -> str:
        try:
            result = self.tech_detection_chain.invoke(
                {
                    "files_info": files_info[:1000],
                    "dependencies": dependencies[:1000],
                }
            )
            return self._normalize(result).strip()
        except Exception as e:
            print(f"⚠️ Technology detection failed: {e}")
            return "Unknown"

    def generate_readme(
        self,
        repo_url: str,
        analysis: str,
        dependencies: str,
        file_structure: str,
        semantic_context: str = "",
    ) -> str:
        try:
            prompt = readme_generation_prompt.invoke(
                {
                    "repo_url": repo_url,
                    "analysis": analysis[:3000],
                    "dependencies": dependencies[:1000],
                    "file_structure": file_structure[:1000],
                    "semantic_context": semantic_context[:1000],
                }
            ).to_string()

            response = self.llm.invoke(prompt)
            return self._normalize(response)

        except Exception as e:
            raise RuntimeError(f"Failed to generate README: {e}")

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    def split_documents(self, documents: List[Document]) -> List[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        return splitter.split_documents(documents)

    def create_document(self, content: str, metadata: dict) -> Document:
        return Document(page_content=content, metadata=metadata)

    def batch_analyze_files(
        self, files: List[Tuple[str, str]]
    ) -> List[str]:
        return [
            self.analyze_file(file_name, file_content)
            for file_name, file_content in files
        ]
