from typing import Dict, List, Tuple
from backend.config.settings import settings
from backend.utils.file_utils import (
    get_priority_files,
    get_dependency_files,
    get_file_structure,
    detect_primary_language,
    read_file_safe
)
from backend.services.langchain_service import LangChainService

class AnalysisService:
    """Service for analyzing repository content"""
    
    def __init__(self):
        """Initialize analysis service"""
        self.langchain_service = LangChainService()
    
    def analyze_repository(self, repo_path: str) -> Dict:
        """
        Complete repository analysis
        
        Args:
            repo_path: Path to cloned repository
            
        Returns:
            Dictionary containing all analysis results
        """
        print("Starting repository analysis...")
        
        # Step 1: Get file structure
        file_structure = get_file_structure(repo_path, max_files=50)
        print(f"File structure extracted ({len(file_structure.split(chr(10)))} files)")
        
        # Step 2: Detect dependencies
        dependencies = get_dependency_files(repo_path)
        deps_text = self._format_dependencies(dependencies)
        print(f"Dependencies detected: {len(dependencies)} files")
        
        # Step 3: Detect primary language
        primary_language = detect_primary_language(repo_path)
        print(f"Primary language: {primary_language}")
        
        # Step 4: Analyze priority files
        file_analyses = self._analyze_files(repo_path)
        print(f"Analyzed {len(file_analyses)} files")
        
        # Step 5: Create semantic context
        semantic_context = self._create_semantic_context(repo_path)
        print(f"Semantic context created")
        
        # Step 6: Detect technologies
        technologies = self._detect_technologies(file_analyses, deps_text)
        print(f"Technologies detected: {technologies}")
        
        return {
            "file_structure": file_structure,
            "dependencies": deps_text,
            "primary_language": primary_language,
            "file_analyses": file_analyses,
            "semantic_context": semantic_context,
            "technologies": technologies,
            "files_analyzed_count": len(file_analyses)
        }
    
    def _analyze_files(self, repo_path: str) -> str:
        """
        Analyze priority files using LangChain
        
        Args:
            repo_path: Repository path
            
        Returns:
            Combined analysis of all files
        """
        priority_files = get_priority_files(repo_path)
        analyses = []
        
        for file_path, file_name in priority_files[:settings.MAX_FILES_TO_ANALYZE]:
            content = read_file_safe(file_path, max_chars=settings.MAX_FILE_SIZE)
            
            if content and not content.startswith("[Error"):
                analysis = self.langchain_service.analyze_file(file_name, content)
                analyses.append(f"\n###  {file_name}\n{analysis}")
        
        return '\n'.join(analyses) if analyses else "No significant files analyzed."
    
    def _format_dependencies(self, dependencies: Dict[str, str]) -> str:
        """
        Format dependencies information
        
        Args:
            dependencies: Dictionary of dependencies
            
        Returns:
            Formatted dependency text
        """
        if not dependencies:
            return "No dependency files detected."
        
        formatted = []
        for tech, content in dependencies.items():
            formatted.append(f"\n**{tech}:**\n```\n{content[:500]}\n```")
        
        return '\n'.join(formatted)
    
    def _create_semantic_context(self, repo_path: str) -> str:
        """
        Create semantic context from repository
        
        Args:
            repo_path: Repository path
            
        Returns:
            Semantic context summary
        """
        try:
            # Get README if exists
            readme_files = ['README.md', 'README.txt', 'README']
            for readme in readme_files:
                readme_path = f"{repo_path}/{readme}"
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        existing_readme = f.read(2000)
                        return f"Existing README found:\n{existing_readme}"
                except:
                    continue
            
            return "No existing README found. Generating from scratch."
        
        except Exception as e:
            return f"Context creation skipped: {str(e)}"
    
    def _detect_technologies(self, file_analyses: str, dependencies: str) -> str:
        """
        Detect technologies using LangChain
        
        Args:
            file_analyses: File analysis text
            dependencies: Dependencies text
            
        Returns:
            Comma-separated technologies
        """
        try:
            technologies = self.langchain_service.detect_technologies(
                files_info=file_analyses[:500],
                dependencies=dependencies[:500]
            )
            return technologies
        except Exception as e:
            print(f"Technology detection failed: {e}")
            return "Unknown"