import os
import tempfile
import shutil
from typing import Optional
from git import Repo, GitCommandError
from urllib.parse import urlparse


class RepositoryService:
    """
    Service for handling Git repository operations
    """

    # ------------------------------------------------------------------
    # Repository Operations
    # ------------------------------------------------------------------

    @staticmethod
    def clone_repository(
        repo_url: str,
        target_dir: Optional[str] = None,
    ) -> str:
        """
        Clone a GitHub repository (shallow clone)

        Args:
            repo_url: GitHub repository URL
            target_dir: Optional target directory (temp dir if None)

        Returns:
            Path to cloned repository

        Raises:
            RuntimeError: If cloning fails
        """
        repo_path = target_dir or tempfile.mkdtemp(prefix="repo_")

        try:
            print(f"Cloning repository: {repo_url}")
            Repo.clone_from(
                repo_url,
                repo_path,
                depth=1,           # shallow clone
                single_branch=True # faster, safer
            )
            print(f"Repository cloned to: {repo_path}")
            return repo_path

        except GitCommandError as e:
            RepositoryService.cleanup_repository(repo_path)
            raise RuntimeError(f"Git clone failed: {e.stderr or e}")

        except Exception as e:
            RepositoryService.cleanup_repository(repo_path)
            raise RuntimeError(f"Failed to clone repository: {e}")

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    @staticmethod
    def cleanup_repository(repo_path: str) -> None:
        """
        Remove a cloned repository directory safely
        """
        if not repo_path:
            return

        try:
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path, ignore_errors=True)
                print(f"🧹 Cleaned up repository: {repo_path}")
        except Exception as e:
            print(f"Cleanup warning ({repo_path}): {e}")

    # ------------------------------------------------------------------
    # Validation & Utilities
    # ------------------------------------------------------------------

    @staticmethod
    def validate_github_url(url: str) -> bool:
        """
        Validate whether a URL looks like a GitHub repository URL
        """
        try:
            parsed = urlparse(url)
            return (
                parsed.scheme in {"http", "https"}
                and "github.com" in parsed.netloc.lower()
                and len(parsed.path.strip("/").split("/")) >= 2
            )
        except Exception:
            return False

    @staticmethod
    def extract_repo_name(repo_url: str) -> str:
        """
        Extract repository name from GitHub URL

        Examples:
            https://github.com/user/repo
            https://github.com/user/repo.git
        """
        try:
            path = urlparse(repo_url).path.rstrip("/")
            name = path.split("/")[-1]
            return name.replace(".git", "") or "unknown-repo"
        except Exception:
            return "unknown-repo"
