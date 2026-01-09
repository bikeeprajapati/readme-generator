# README Generator

A web application that automatically generates professional README.md files from GitHub repositories using LangChain and AI.

## Project Structure

```
readme-generator/
├── app.py                 # FastAPI backend
├── Frontend UI
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd readme-generator
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the application**
```bash
python app.py
# or
uvicorn app:app --reload
```

6. **Open the frontend**
Open `index.html` in your browser or serve it using:
```bash
python -m http.server 3000
```

## API Endpoints

- `GET /` - Root endpoint
- `POST /generate-readme` - Generate README from repo URL
- `GET /health` - Health check

## Technologies Used

- FastAPI
- LangChain
- Python
- HTML/CSS/JavaScript

## Development

Add your implementation in `app.py` in the `generate_readme` function.

## Contributing

Feel free to submit issues and pull requests.

## License

MIT