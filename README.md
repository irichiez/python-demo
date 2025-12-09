# Translation Service - Python Demo

A REST API service built with FastAPI that translates English messages to multiple languages using OpenAI's GPT models.

## Features

- RESTful API with GET endpoint for translation
- Support for 5 languages: French, Spanish, Italian, Portuguese, Romanian
- OpenAI integration for high-quality translations
- Comprehensive error handling and logging
- Full test coverage
- Configuration management via environment variables

## Project Structure

```
python-demo/
├── main.py              # FastAPI application entry point
├── controller.py        # REST controller with translation endpoint
├── service.py           # Service layer with OpenAI integration
├── config.py            # Configuration management
├── test_translation.py  # Comprehensive test suite
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── README.md            # This file
```

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone or navigate to the project directory:
```bash
cd python-demo
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

5. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Service

### Development Mode

Run the service using uvicorn:
```bash
python main.py
```

Or directly with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The service will be available at `http://localhost:8000`

### API Documentation

Once the service is running, you can access:
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## API Usage

### Translate Endpoint

**GET** `/api/v1/translate`

Translates an English message to the specified target language.

**Query Parameters:**
- `message` (required): The English message to translate
- `language` (required): Target language - one of: `french`, `spanish`, `italian`, `portuguese`, `romanian`

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/translate?message=Hello%2C%20how%20are%20you%3F&language=french"
```

**Example Response:**
```json
{
  "original_message": "Hello, how are you?",
  "translated_message": "Bonjour, comment allez-vous?",
  "target_language": "french"
}
```

**Example using Python requests:**
```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/translate",
    params={
        "message": "Hello, how are you?",
        "language": "french"
    }
)
print(response.json())
```

### Health Check Endpoints

- **GET** `/` - Service information
- **GET** `/health` - Health check

## Testing

Run the test suite:
```bash
pytest test_translation.py -v
```

Run with coverage:
```bash
pytest test_translation.py --cov=. --cov-report=html
```

## Configuration

Configuration is managed through environment variables (loaded from `.env` file):

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `OPENAI_MODEL` (optional): OpenAI model to use (default: `gpt-3.5-turbo`)
- `APP_NAME` (optional): Application name (default: "Translation Service")
- `APP_VERSION` (optional): Application version (default: "1.0.0")
- `DEBUG` (optional): Enable debug mode (default: `false`)
- `LOG_LEVEL` (optional): Logging level (default: `INFO`)

## Error Handling

The service includes comprehensive error handling:

- **400 Bad Request**: Invalid parameters (empty message, invalid language)
- **422 Unprocessable Entity**: Missing required parameters
- **500 Internal Server Error**: Service errors, API failures
- **503 Service Unavailable**: OpenAI API connection issues

All errors are logged with appropriate detail levels.

## Supported Languages

- `french` - French
- `spanish` - Spanish
- `italian` - Italian
- `portuguese` - Portuguese
- `romanian` - Romanian

## Architecture

The project follows a clean architecture pattern:

1. **Controller Layer** (`controller.py`): Handles HTTP requests/responses, validation
2. **Service Layer** (`service.py`): Business logic, OpenAI integration
3. **Configuration Layer** (`config.py`): Environment-based configuration management
4. **Main Application** (`main.py`): FastAPI app setup, middleware, routing

## Logging

The service uses Python's standard logging module with configurable log levels. Logs include:
- Request/response information
- Translation operations
- Error details with stack traces
- Service initialization

## License

This is a demo project for educational purposes.

