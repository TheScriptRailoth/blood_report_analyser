# Blood Test Report Analyzer

A FastAPI-based application that analyzes blood test reports using local LLM (Llama 2 via Ollama) to provide medical insights and recommendations.

## 🚀 Features

- **Local LLM Processing**: Uses Llama 2 running locally via Ollama (no API keys required)
- **PDF Analysis**: Upload and analyze blood test reports in PDF format
- **Medical Insights**: Get detailed medical analysis and recommendations
- **RESTful API**: Simple HTTP endpoints for easy integration
- **Free & Open Source**: No paid services or API keys needed

## 🐛 Bugs Found and Fixed

### 1. **LLM Configuration Error**
- **Issue**: The default model `llama3` was passed without specifying the LLM provider
- **Fix**: Integrated local Ollama LLM using a custom `OllamaLLM` class, eliminating the need for cloud providers
- **Code**: Created `OllamaLLM` class that directly calls your local Llama 2 model

### 2. **Invalid LLM Import**
- **Issue**: Attempted to import `CrewLiteLLM` and `ChatLiteLLM`, which do not exist in CrewAI
- **Fix**: Replaced with direct Ollama integration:
```python
import ollama

class OllamaLLM:
    def __init__(self, model='llama2'):
        self.model = model
    def __call__(self, prompt, **kwargs):
        response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
```

### 3. **CrewAI Agent System Conflicts**
- **Issue**: `crewai.Agent` system forced usage of cloud LLM providers via `litellm`, causing persistent errors
- **Fix**: Bypassed CrewAI Agent system entirely and created custom `DoctorAgent` class
- **Code**: Replaced complex CrewAI workflow with direct LLM calls

### 4. **Incorrect Tool Class Implementation**
- **Issue**: `BaseTool` was wrongly imported or implemented
- **Fix**: Corrected import and implementation:
```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class BloodTestReportTool(BaseTool):
    name: str = "read_data_tool"
    description: str = "Reads and returns blood report content from a PDF file"
    args_schema: Type[BaseModel] = BloodTestReportInput
```

### 5. **Pydantic ValidationError**
- **Issue**: StructuredTool or function-based tools were passed directly to CrewAI without conforming to expected formats
- **Fix**: Migrated tools to class-based implementation as required by CrewAI and Pydantic

### 6. **LangChain & LangChainCommunity Deprecation**
- **Issue**: Old imports from `langchain.tools` triggered deprecation warnings
- **Fix**: Updated to use:
```python
from langchain_community.document_loaders import PyPDFLoader
from crewai_tools import SerperDevTool
```

### 7. **Tool Not Callable by Agent**
- **Issue**: The `read_data_tool` (PDF parser) wasn't being called properly due to incorrect instantiation
- **Fix**: Ensured it was instantiated correctly:
```python
read_data_tool = BloodTestReportTool()
```

### 8. **Uvicorn Not Recognized**
- **Issue**: Uvicorn was not recognized in PowerShell
- **Fix**: Used `python -m uvicorn main:app --reload` instead of `uvicorn main:app`

### 9. **FastAPI Multipart Error**
- **Issue**: Missing `python-multipart` caused multipart/form-data parsing to fail
- **Fix**: Installed required dependency:
```bash
pip install python-multipart
```

### 10. **litellm Provider Errors**
- **Issue**: Persistent errors about LLM provider not being specified
- **Fix**: Completely removed litellm dependency and switched to direct Ollama integration

### 11. **Unhandled Exception Logging**
- **Issue**: Poor error handling and debugging information
- **Fix**: Added comprehensive error handling and debug logs for better traceability

## 📋 Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Llama 2 model downloaded in Ollama

## 🛠️ Installation

### 1. **Install Ollama**
```bash
# Download and install from https://ollama.com/download
# Then pull Llama 2 model
ollama pull llama2
```

### 2. **Clone and Setup Project**
```bash
git clone https://github.com/TheScriptRailoth/blood_report_analyser.git
cd blood-test-analyser-debug
```

### 3. **Create Virtual Environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 4. **Install Dependencies**
```bash
pip install fastapi uvicorn python-multipart ollama crewai langchain-community pydantic python-dotenv
```

### 5. **Start Ollama Server**
```bash
# Make sure Ollama is running with Llama 2
ollama run llama2
```

## 🚀 Usage

### 1. **Start the API Server**
```bash
python -m uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

### 2. **Access API Documentation**
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 📚 API Documentation

### **Health Check**
```http
GET /
```
**Response:**
```json
{
  "message": "Blood Test Report Analyser API is running"
}
```

### **Analyze Blood Test Report**
```http
POST /analyze
Content-Type: multipart/form-data
```

**Parameters:**
- `file` (required): PDF file containing blood test report
- `query` (optional): Custom query for analysis (default: "Summarise my Blood Test Report")

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@blood_test_report.pdf" \
  -F "query=Analyze my blood test results and provide recommendations"
```

**Response:**
```json
{
  "status": "success",
  "query": "Analyze my blood test results and provide recommendations",
  "analysis": "Based on your blood test results, I can see several important markers...",
  "file_processed": "blood_test_report.pdf"
}
```

**Error Response:**
```json
{
  "detail": "Error processing blood report: <error details>"
}
```

## 🏗️ Project Structure

```
blood-test-analyser-debug/
├── main.py              # FastAPI application and endpoints
├── agents.py            # LLM integration and agent definitions
├── tools.py             # PDF processing and utility tools
├── task.py              # Task definitions (legacy, not used)
├── data/                # Directory for uploaded PDF files
├── outputs/             # Directory for generated outputs
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
LLM_PROVIDER=groq
```

### Ollama Configuration
- Default model: `llama2`
- Server URL: `http://localhost:11434` (default)
- Model can be changed in `agents.py` by modifying the `OllamaLLM` class

## 🧪 Testing

### 1. **Test Health Endpoint**
```bash
curl http://127.0.0.1:8000/
```

### 2. **Test File Upload**
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/sample.pdf" \
  -F "query=Summarize this blood test report"
```

### 3. **Using Python Requests**
```python
import requests

url = "http://127.0.0.1:8000/analyze"
files = {"file": open("data/sample.pdf", "rb")}
data = {"query": "Analyze this blood test report"}

response = requests.post(url, files=files, data=data)
print(response.json())
```

## 🔍 Troubleshooting

### **Common Issues**

1. **"Ollama connection failed"**
   - Ensure Ollama is running: `ollama run llama2`
   - Check if Llama 2 model is downloaded: `ollama list`

2. **"File upload failed"**
   - Ensure `python-multipart` is installed
   - Check file format (PDF only)
   - Verify file size (not too large)

3. **"LLM response error"**
   - Check Ollama server status
   - Verify model is loaded: `ollama ps`
   - Check system resources (RAM, CPU)

4. **"Import errors"**
   - Ensure virtual environment is activated
   - Install all dependencies: `pip install -r requirements.txt`

### **Debug Mode**
Enable debug logging by setting environment variable:
```bash
export PYTHONPATH=.
python -m uvicorn main:app --reload --log-level debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) for local LLM hosting
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [CrewAI](https://github.com/joaomdmoura/crewAI) for the original agent framework inspiration
- [Llama 2](https://ai.meta.com/llama/) for the language model

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub
4. Check the debug logs for detailed error information
