import os
from pathlib import Path
from typing import List, Dict, Tuple


# ------------------------------------------------------------------
# File Reading
# ------------------------------------------------------------------

def read_file_safe(file_path: str, max_chars: int = 5000) -> str:
    """
    Safely read file content with character limit
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(max_chars)
    except Exception as e:
        return f"[Error reading file: {e}]"


# ------------------------------------------------------------------
# File Type Helpers
# ------------------------------------------------------------------

def get_file_extension(filename: str) -> str:
    """Return lowercase file extension"""
    return Path(filename).suffix.lower()


def is_code_file(filename: str) -> bool:
    """Check if file is a source code file"""
    return get_file_extension(filename) in {
        ".py", ".js", ".ts", ".jsx", ".tsx",
        ".go", ".rs", ".java", ".cpp", ".c", ".h",
        ".cs", ".php", ".rb", ".swift", ".kt",
        ".scala", ".r", ".m", ".sql",
    }


def is_config_file(filename: str) -> bool:
    """Check if file is a configuration / dependency file"""
    return filename.lower() in {
        "package.json",
        "requirements.txt",
        "cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "gemfile",
        "composer.json",
        "setup.py",
        "pyproject.toml",
        "tsconfig.json",
        ".env.example",
    }


# ------------------------------------------------------------------
# Directory Helpers
# ------------------------------------------------------------------

def should_skip_directory(dirname: str) -> bool:
    """Check if directory should be skipped during traversal"""
    skip_dirs = {
        "node_modules",
        "__pycache__",
        "venv",
        "env",
        ".git",
        ".vscode",
        ".idea",
        "dist",
        "build",
        "target",
        ".next",
    }
    return dirname.startswith(".") or dirname in skip_dirs


# ------------------------------------------------------------------
# Repository Structure
# ------------------------------------------------------------------

def get_file_structure(directory: str, max_files: int = 50) -> str:
    """
    Generate a tree-like file structure (flat list)
    """
    root = Path(directory)
    files: List[str] = []

    for path in root.rglob("*"):
        if any(should_skip_directory(p.name) for p in path.parents):
            continue

        if path.is_file():
            files.append(str(path.relative_to(root)))

        if len(files) >= max_files:
            break

    return "\n".join(files)


# ------------------------------------------------------------------
# Language Detection
# ------------------------------------------------------------------

def detect_primary_language(directory: str) -> str:
    """
    Detect primary programming language by file frequency
    """
    language_extensions = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".cs": "C#",
        ".php": "PHP",
        ".rb": "Ruby",
    }

    counts: Dict[str, int] = {}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not should_skip_directory(d)]

        for file in files:
            ext = get_file_extension(file)
            if ext in language_extensions:
                counts[ext] = counts.get(ext, 0) + 1

    if not counts:
        return "Unknown"

    dominant_ext = max(counts, key=counts.get)
    return language_extensions[dominant_ext]


# ------------------------------------------------------------------
# Priority Files
# ------------------------------------------------------------------

def get_priority_files(directory: str, limit: int = 10) -> List[Tuple[str, str]]:
    """
    Get important source files to analyze first
    """
    priority_names = {
        "main.py", "app.py", "__init__.py",
        "index.js", "main.js", "app.js",
        "index.ts", "main.go", "main.rs",
        "App.jsx", "App.tsx",
        "main.java", "Program.cs",
    }

    results: List[Tuple[str, str]] = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not should_skip_directory(d)]

        for file in files:
            if file in priority_names or is_code_file(file):
                file_path = os.path.join(root, file)
                results.append((file_path, file))

                if len(results) >= limit:
                    return results

    return results


# ------------------------------------------------------------------
# Dependency Detection
# ------------------------------------------------------------------

def get_dependency_files(directory: str) -> Dict[str, str]:
    """
    Locate and read dependency/configuration files
    """
    dependency_map = {
        "package.json": "Node.js / JavaScript",
        "requirements.txt": "Python",
        "pyproject.toml": "Python",
        "Cargo.toml": "Rust",
        "go.mod": "Go",
        "pom.xml": "Java (Maven)",
        "build.gradle": "Java (Gradle)",
        "Gemfile": "Ruby",
        "composer.json": "PHP",
    }

    found: Dict[str, str] = {}

    for filename, tech in dependency_map.items():
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            found[tech] = read_file_safe(path, max_chars=3000)

    return found
