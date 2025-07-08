# VectorShift Backend API

A FastAPI-based backend service for the VectorShift pipeline builder application. This API analyzes visual pipelines, counts nodes and edges, and determines if the pipeline forms a Directed Acyclic Graph (DAG).

## 🚀 Features

- **Pipeline Analysis**: Count nodes and edges in visual pipelines
- **DAG Detection**: Determine if pipelines contain cycles using NetworkX
- **CORS Support**: Cross-origin requests enabled for frontend integration
- **Real-time Validation**: Fast pipeline validation and analysis
- **RESTful API**: Clean, documented endpoints

## 🛠️ Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **Pydantic**: Data validation using Python type annotations
- **NetworkX**: Graph analysis library for DAG detection
- **Python 3.12**: Latest stable Python version

## 📋 Prerequisites

- Python 3.11+ (3.12 recommended)
- pip (Python package manager)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd vectorshift-backend
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Alternative: Install packages individually
pip install fastapi uvicorn pydantic networkx
```

### 4. Verify Installation
```bash
python -c 'import fastapi; print("FastAPI installed successfully")'
python -c 'import uvicorn; print("Uvicorn installed successfully")'
python -c 'import networkx; print("NetworkX installed successfully")'
```

## 🚀 Running the Application

### Development Server
```bash
# Start the development server with auto-reload
uvicorn main:app --reload

# Custom host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Server
```bash
# Start production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

### Automatic Documentation
FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Endpoints

#### `GET /`
Health check endpoint
```json
{
  "message": "VectorShift Pipeline Parser API",
  "status": "running"
}
```

#### `GET /test`
Test endpoint for connectivity verification
```json
{
  "test": "success",
  "backend": "working with Python 3.12"
}
```

#### `POST /pipelines/parse`
Analyze a pipeline and return statistics

**Request Body:**
```json
{
  "nodes": [
    {
      "id": "node-1",
      "type": "input",
      "position": {"x": 100, "y": 100},
      "data": {}
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "source": "node-1",
      "target": "node-2",
      "sourceHandle": "output",
      "targetHandle": "input"
    }
  ]
}
```

**Response:**
```json
{
  "num_nodes": 2,
  "num_edges": 1,
  "is_dag": true
}
```

## 🧪 Testing

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:8000/

# Test pipeline analysis
curl -X POST http://localhost:8000/pipelines/parse \
  -H "Content-Type: application/json" \
  -d '{
    "nodes": [
      {"id": "1", "type": "input", "position": {"x": 0, "y": 0}, "data": {}}
    ],
    "edges": []
  }'
```

### Browser Testing
1. Start the server: `uvicorn main:app --reload`
2. Open: http://localhost:8000
3. Test interactive docs: http://localhost:8000/docs

## 🏗️ Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Git ignore rules
├── venv/               # Virtual environment (gitignored)
└── __pycache__/        # Python cache (gitignored)
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for environment-specific configurations:

```bash
# .env
DEBUG=True
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
```

### CORS Configuration
The API is configured to allow all origins for development. For production, update the CORS settings in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify exact domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 📊 DAG Detection Algorithm

The backend uses NetworkX to detect cycles in the pipeline:

1. **Graph Construction**: Creates a directed graph from nodes and edges
2. **Cycle Detection**: Uses NetworkX's `is_directed_acyclic_graph()` function
3. **Result**: Returns `true` if no cycles exist, `false` if cycles are detected

### Supported Pipeline Elements
- **Nodes**: Any node type (input, output, LLM, text, etc.)
- **Edges**: Connections between nodes with source/target handles
- **Validation**: Ensures all referenced nodes exist

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Use different port
uvicorn main:app --port 8001 --reload
```

#### Import Errors
```bash
# Verify virtual environment is activated
which python

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### CORS Errors
- Ensure CORS middleware is properly configured
- Check that frontend is making requests to correct URL
- Verify `allow_origins` includes your frontend domain

#### Python Version Issues
```bash
# Check Python version
python --version

# Use specific Python version
python3.12 -m uvicorn main:app --reload
```

### Debug Mode
Enable debug logging by setting environment variable:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
export DEBUG=True
uvicorn main:app --reload --log-level debug
```

## 🤝 Development

### Adding New Endpoints
1. Add endpoint function in `main.py`
2. Use appropriate HTTP method decorator (`@app.get`, `@app.post`, etc.)
3. Add Pydantic models for request/response validation
4. Update this README with endpoint documentation

### Code Style
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Add docstrings for functions and classes

### Dependencies
To add new dependencies:
```bash
pip install <package-name>
pip freeze > requirements.txt
```

## 📄 License

This project is part of the VectorShift technical assessment.

## 🆘 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Verify all prerequisites are installed
3. Ensure virtual environment is activated
4. Check server logs for error details

## 🔄 Integration with Frontend

This backend is designed to work with the VectorShift React frontend:

1. **Frontend URL**: Typically runs on `http://localhost:3000`
2. **API Calls**: Frontend sends pipeline data to `/pipelines/parse`
3. **Response Handling**: Frontend displays node count, edge count, and DAG status
4. **CORS**: Configured to accept requests from frontend origin

For frontend setup instructions, see the frontend README.