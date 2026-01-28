# 📝 AI-Powered README Generator

> **A LangChain learning project that generates professional README.md files for any GitHub repository**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-orange.svg)](https://python.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Project Overview

This project was built as a **capstone for my LangChain learning journey**. It demonstrates practical implementation of LangChain concepts in a real-world application that solves an actual problem: automating documentation generation.

### The Problem
- Developers spend hours writing README files
- Many repositories have incomplete or outdated documentation  
- Documentation quality varies significantly across projects

### The Solution
An AI-powered web application that:
- Analyzes any public GitHub repository
- Understands project structure and dependencies
- Generates comprehensive, professional README.md files automatically
- Provides intelligent fallbacks when AI models are unavailable

## ✨ Features

- 🤖 **AI-Powered Analysis** - Uses HuggingFace models via LangChain
- 📊 **Smart Detection** - Automatically identifies technologies and frameworks
- 🎨 **Beautiful UI** - Modern dark-mode interface with smooth animations
- 🔄 **Intelligent Fallbacks** - Graceful degradation when APIs are unavailable
- ⚡ **Fast & Efficient** - Async operations and optimized processing
- 🐳 **Docker Ready** - Containerized for easy deployment
- 📚 **Well Documented** - Comprehensive code documentation and examples

## 🧠 LangChain Concepts Demonstrated

This project showcases **10+ core LangChain concepts** learned during my study:

### 1. **LLM Integration**
```python
from langchain_huggingface import HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xxl",
    temperature=0.7,
    max_new_tokens=2048
)
```

### 2. **Prompt Templates**
Structured, reusable prompts for consistent outputs:
```python
from langchain_core.prompts import PromptTemplate

file_analysis_prompt = PromptTemplate(
    input_variables=["file_name", "file_content"],
    template="Analyze this code file..."
)
```

### 3. **LLM Chains**
Sequential processing with chained operations:
```python
analysis_chain = file_analysis_prompt | llm
result = analysis_chain.invoke({"file_name": "app.py", "file_content": code})
```

### 4. **Document Processing**
```python
from langchain_core.documents import Document

doc = Document(page_content=content, metadata={"source": filename})
```

### 5. **Text Splitting**
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)
```

### 6. **Output Parsing**
Structured response handling for consistent outputs

### 7. **Error Handling**
Robust error handling with graceful fallbacks

### 8. **Batch Processing**
Efficient processing of multiple files

### 9. **Semantic Analysis**
Context extraction from repository content

### 10. **Production Patterns**
Service layer architecture, dependency injection, async operations

## 🛠️ Technology Stack

### Backend
- **FastAPI 0.115+** - Modern async web framework
- **LangChain 0.3+** - LLM orchestration framework
- **HuggingFace Hub** - AI model integration
- **Pydantic v2** - Data validation with improved performance
- **Python 3.8+** - With type hints and async support

### AI/ML
- **LangChain Core** - Foundation for LLM applications
- **LangChain Community** - Additional integrations
- **HuggingFace Transformers** - Model support
- **Sentence Transformers** - Embeddings generation

### DevOps
- **Docker** - Containerization
- **Uvicorn** - ASGI server
- **GitPython** - Repository management

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- HuggingFace API token ([Get one here](https://huggingface.co/settings/tokens))
- Git

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/readme-generator.git
cd readme-generator

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your HUGGINGFACE_API_KEY

# 5. Run the application
python run.py
```

The API will be available at `http://localhost:8000`

### Using Docker

```bash
# Build the image
docker build -t readme-generator .

# Run the container
docker run -p 8000:8000 --env-file .env readme-generator
```

## 🚀 Usage

### Web Interface

1. Open `frontend/index.html` in your browser
2. Enter any public GitHub repository URL
3. Click "Generate README"
4. Copy or download the generated README

### API Usage

```bash
curl -X POST "http://localhost:8000/generate-readme" \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/username/repo"}'
```

### Python Client

```python
import requests

response = requests.post(
    "http://localhost:8000/generate-readme",
    json={"repo_url": "https://github.com/username/repo"}
)

readme = response.json()["readme_content"]
print(readme)
```

## 📁 Project Structure

```
readme-generator/
├── backend/
│   ├── main.py                      # FastAPI application
│   ├── config/
│   │   └── settings.py              # Configuration with Pydantic
│   ├── services/
│   │   ├── langchain_service.py     # LangChain operations
│   │   ├── analysis_service.py      # Repository analysis
│   │   └── repository_service.py    # Git operations
│   ├── models/
│   │   └── schemas.py               # API models
│   ├── utils/
│   │   ├── prompt_templates.py      # LangChain prompts
│   │   └── file_utils.py            # File operations
│   └── api/
│       └── routes.py                # API endpoints
├── frontend/
│   └── index.html                   # Modern UI
├── docs/
│   ├── LANGCHAIN_CONCEPTS.md        # Detailed explanations
│   └── TROUBLESHOOTING.md           # Common issues
├── tests/
│   └── test_api.py                  # Unit tests
├── .env.example                     # Environment template
├── requirements.txt                 # Dependencies
├── Dockerfile                       # Container config
└── README.md                        # This file
```

## 🎓 Learning Journey

### What I Learned

**Week 1: Foundations**
- Understanding LangChain architecture
- Working with prompt templates
- Basic LLM integration

**Week 2: Advanced Concepts**
- Building complex chains
- Document processing and splitting
- Output parsing and validation

**Week 3: Production Readiness**
- Error handling strategies
- Fallback mechanisms
- Performance optimization

**Week 4: Deployment**
- Docker containerization
- API design best practices
- Frontend integration

### Key Takeaways

1. **LangChain simplifies LLM orchestration** - What would take hundreds of lines is now just a few
2. **Prompt engineering is crucial** - Good prompts = good outputs
3. **Always have fallbacks** - AI models can be unreliable
4. **Production AI ≠ Tutorial AI** - Real-world needs error handling, monitoring, and graceful degradation

## 🔧 Configuration

### Environment Variables

```bash
# Required
HUGGINGFACE_API_KEY=hf_your_token_here
HUGGINGFACE_MODEL=google/flan-t5-xxl

# Optional
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
TEMPERATURE=0.7
MAX_TOKENS=2048
```

### Model Options

```bash
# Fast & Reliable (Recommended)
HUGGINGFACE_MODEL=google/flan-t5-xxl

# High Quality
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.2

# Code-Focused
HUGGINGFACE_MODEL=HuggingFaceH4/zephyr-7b-beta
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=backend tests/

# Check setup
python check_setup.py
```

## 📊 Performance

- **Average generation time:** 30-60 seconds
- **Repository size limit:** Up to 50 files analyzed
- **Supported languages:** Python, JavaScript, TypeScript, Java, Go, Rust, and more
- **Fallback success rate:** 100% (always generates a README)

## 🤝 Contributing

Contributions are welcome! This project is open for:

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🧪 Test coverage
- 🎨 UI/UX enhancements

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@bikeeprajapati](https://github.com/bikeeprajapati)
- LinkedIn: [Bikee Prajapati](https://www.linkedin.com/in/bikee-prajapati9898/)
- Email: your.email@example.com

## 🙏 Acknowledgments

- **LangChain Team** - For the amazing framework
- **HuggingFace** - For model hosting and APIs
- **FastAPI** - For the excellent web framework
- **Open Source Community** - For inspiration and support

## 📚 Resources

- [LangChain Documentation](https://python.langchain.com/docs/)
- [HuggingFace Models](https://huggingface.co/models)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [My LangChain Learning Notes](docs/LANGCHAIN_CONCEPTS.md)

## 🎯 Future Enhancements

- [ ] Support for private repositories
- [ ] Multiple README templates
- [ ] Multi-language support
- [ ] README quality scoring
- [ ] Integration with GitLab/Bitbucket
- [ ] CLI tool version
- [ ] VS Code extension
- [ ] Batch processing for multiple repos

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

**Built with  using LangChain**


</div>