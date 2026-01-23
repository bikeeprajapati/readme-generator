from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# File Analysis Prompt Template (LangChain v0.3+)
FILE_ANALYSIS_TEMPLATE = """You are a code analysis expert. Analyze the following file and extract key information.

File: {file_name}
Content:
{file_content}

Provide a brief summary (2-3 sentences) of:
1. What this file does
2. Its purpose in the project
3. Key functions or components

Keep your response concise and technical."""

file_analysis_prompt = PromptTemplate.from_template(FILE_ANALYSIS_TEMPLATE)

# README Generation Prompt Template
README_GENERATION_TEMPLATE = """You are an expert technical writer specializing in creating comprehensive README.md files.

Create a professional README.md based on the following repository analysis:

**Repository URL:** {repo_url}

**Project Analysis:**
{analysis}

**Dependencies Found:**
{dependencies}

**File Structure:**
{file_structure}

**Additional Context:**
{semantic_context}

Generate a complete, professional README.md with these sections:

# [Project Title]
Write a creative, descriptive title based on the repository name and content.

## Description
2-3 sentences explaining what the project does and its main purpose.

## Features
- List 3-5 key features as bullet points
- Focus on what makes this project useful

## Technologies Used
List all technologies, frameworks, and libraries detected in the project.

## Installation

Provide step-by-step installation instructions:
```bash
# Clone the repository
git clone [repo-url]

# Install dependencies
[appropriate commands based on detected tech stack]
```

## Usage

Provide clear usage examples with code blocks if applicable.

## Project Structure

Brief overview of the main files and folders.

## Contributing

Standard contributing guidelines.

## License

Mention the license (default to MIT if none found).

---

**IMPORTANT FORMATTING RULES:**
- Use proper Markdown syntax
- Include code blocks with language specifications
- Use headers (##) for sections
- Make it engaging and professional
- Keep it concise but informative
- Use badges if appropriate (build status, version, etc.)

Generate the README now:"""

readme_generation_prompt = PromptTemplate.from_template(README_GENERATION_TEMPLATE)

# Technology Detection Prompt
TECH_DETECTION_TEMPLATE = """Based on the following file content and names, identify all technologies, frameworks, and programming languages used:

Files analyzed:
{files_info}

Dependencies:
{dependencies}

List all technologies in a simple comma-separated format.
Example: Python, FastAPI, React, PostgreSQL, Docker

Technologies:"""

tech_detection_prompt = PromptTemplate.from_template(TECH_DETECTION_TEMPLATE)

# Additional prompt for advanced analysis
PROJECT_SUMMARY_TEMPLATE = """Analyze this project and provide a concise summary:

Repository: {repo_url}
Primary Language: {primary_language}
Files: {file_count}

Based on the code analysis:
{analysis}

Provide a 2-3 sentence summary of what this project does and who might use it."""

project_summary_prompt = PromptTemplate.from_template(PROJECT_SUMMARY_TEMPLATE)