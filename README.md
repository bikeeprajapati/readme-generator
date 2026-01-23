# 📝 README Generator v2.0

An AI-powered web application that automatically generates professional README.md files from GitHub repositories using **HuggingFace models** and **LangChain v0.3+**.

## 🌟 Features

- 🤖 **AI-Powered**: Uses latest HuggingFace LLMs for intelligent README generation
- 🔗 **LangChain v0.3+**: Built with the latest LangChain architecture
- 📊 **Smart Analysis**: Analyzes code structure, dependencies, and project patterns
- 🎯 **Professional Output**: Generates well-structured, comprehensive READMEs
- 🚀 **Fast & Efficient**: Optimized for performance with async operations
- 🔧 **Highly Configurable**: Easy model and parameter customization
- 📦 **Modern Stack**: FastAPI 0.115+, Pydantic v2, Python 3.8+

## 📁 Project Structure

```
readme-generator/
├── backend/
│   ├── main.py                      # FastAPI app entry point
│   ├── config/
│   │   └── settings.py              # Pydantic v2 settings
│   ├── services/
│   │   ├── repository_service.py    # Git operations
│   │   ├── analysis_service.py      # Repository analysis
│   │   └── langchain_service.py     # LangChain v0.3+ operations
│   ├── models/
│   │   └── schemas.py               # Pydantic v2 models
│   ├── utils/
│   │   ├── file_utils.py            # File operations
│   │   └── prompt_templates.py      # LangChain prompts
│   └── api/
│       └── routes.py                # API endpoints
├── frontend/
│   └── index.html                   # Web interface
├── temp/                            # Temporary repos (auto-cleaned)
├── .env.example                     # Environment template
├── requirements.txt                 # Latest dependencies
├── run.py                           # Entry point
└── README.md
```

## 🛠️ Technologies Used

### Backend
- **FastAPI 0.115+** - Modern async web framework
- **Pydantic v2** - Data validation with improved performance
- **LangChain 0.3+** - Latest LLM orchestration framework
- **Python 3.8+** - With type hints and async support

### AI/ML
- **HuggingFace Transformers 4.47+** - Latest model support
- **langchain-huggingface 0.1+** - HuggingFace integration
- **HuggingFace Hub 0.26+** - Model repository access

### Tools
- **GitPython 3.1+** - Repository management
- **Uvicorn 0.32+** - ASGI server with HTTP/2 support

## 📋 Prerequisites

- **Python 3.8 or higher** (3.10+ recommended)
- **HuggingFace Account** - [Sign up here](https://huggingface.co/join)
- **HuggingFace API Token** - [Get token here](https://huggingface.co/settings/tokens)
- **Git** - Installed on your system

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd readme-generator
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and configure:
# 1. Add your HuggingFace API token
# 2. Choose your preferred model
# 3. Adjust other settings as needed
```

**Important**: Get your HuggingFace token from https://huggingface.co/settings/tokens

### 5. Run the Application

```bash
# Method 1: Using run.py (recommended)
python run.py

# Method 2: Using uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 💻 Usage

### Using the Web Interface

1. Open `frontend/index.html` in your browser
2. Enter a GitHub repository URL (e.g., `https://github.com/username/repo`)
3. Click "Generate README"
4. Wait for analysis and generation
5. Copy the generated README

### Using the API Directly

```bash
# Example cURL request
curl -X POST "http://localhost:8000/generate-readme" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/username/repository"
  }'
```

### Python Example

```python
import requests

response = requests.post(
    "http://localhost:8000/generate-readme",
    json={"repo_url": "https://github.com/username/repo"}
)

readme = response.json()["readme_content"]
print(readme)
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API info |
| `/health` | GET | Health check with model info |
| `/generate-readme` | POST | Generate README from repo URL |
| `/models` | GET | Get current model information |
| `/docs` | GET | Interactive API documentation (Swagger) |
| `/redoc` | GET | Alternative API documentation (ReDoc) |

## 🧠 LangChain Concepts Applied (v0.3+)

This project demonstrates the following **modern LangChain concepts**:

1. **HuggingFaceEndpoint** - Latest HF integration
2. **Prompt Templates** - Reusable prompt patterns
3. **Chain Invocation** - New `.invoke()` API
4. **Document Processing** - File content handling
5. **Text Splitters** - RecursiveCharacterTextSplitter
6. **Pydantic v2 Integration** - Type-safe models
7. **Async Operations** - Modern async patterns
8. **Lifespan Events** - Startup/shutdown handling
9. **Response Handling** - Content extraction
10. **Batch Processing** - Efficient file analysis

## ⚙️ Configuration

### Model Selection

Edit `.env` to choose your model:

```bash
# Recommended models (as of 2024)
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.3      # Best balance
HUGGINGFACE_MODEL=meta-llama/Meta-Llama-3-8B-Instruct     # High quality
HUGGINGFACE_MODEL=microsoft/phi-2                          # Fast & efficient
HUGGINGFACE_MODEL=HuggingFaceH4/zephyr-7b-beta            # Great for code
```

### Model Parameters

```bash
# Fine-tune generation
TEMPERATURE=0.7        # Creativity (0.0-1.0)
MAX_TOKENS=2048        # Response length
TOP_P=0.95            # Nucleus sampling
TIMEOUT=120           # Request timeout (seconds)
```

### Processing Limits

```bash
MAX_FILES_TO_ANALYZE=10    # Files to analyze
MAX_FILE_SIZE=5000         # Characters per file
```

## 🚀 Performance Tips

1. **Choose the right model**: Smaller models (phi-2) are faster, larger models (Llama-3) are more accurate
2. **Adjust MAX_FILES_TO_ANALYZE**: Reduce for faster processing
3. **Use caching**: Set `USE_CACHE=True` in `.env`
4. **Optimize token limits**: Balance `MAX_TOKENS` vs speed

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=backend tests/

# Run specific test
pytest tests/test_api.py -v
```

## 📊 Example Output

The generator creates README files with:

✅ Project title and description  
✅ Key features list  
✅ Technology stack detection  
✅ Installation instructions  
✅ Usage examples with code  
✅ Project structure overview  
✅ Contributing guidelines  
✅ License information  

## 🔧 Troubleshooting

### Common Issues

**Issue**: `Failed to initialize HuggingFace LLM`
- **Solution**: Check your API token in `.env` file
- **Solution**: Verify token has proper permissions

**Issue**: `Model loading timeout`
- **Solution**: Increase `TIMEOUT` in `.env`
- **Solution**: Try a smaller/faster model

**Issue**: `Repository clone failed`
- **Solution**: Check repository URL is correct
- **Solution**: Ensure repository is public

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add type hints to all functions
- Write tests for new features
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain) v0.3+
- Powered by [HuggingFace](https://huggingface.co/) Transformers
- [FastAPI](https://fastapi.tiangolo.com/) framework
- [Pydantic](https://docs.pydantic.dev/) v2

## 📈 Roadmap

- [ ] Add support for GitLab and Bitbucket
- [ ] Implement README templates
- [ ] Add multi-language support
- [ ] Create CLI tool
- [ ] Add README quality scoring
- [ ] Support for private repositories

## 📧 Support

- 📖 Check the [documentation](docs/)
- 🐛 Report bugs via [GitHub Issues](https://github.com/yourusername/readme-generator/issues)
- 💬 Discussions in [GitHub Discussions](https://github.com/yourusername/readme-generator/discussions)

---

**Built with ❤️ using the latest LangChain v0.3+ and HuggingFace models**

**Happy README Generating! 🎉**