# AI Legal Document Assistant - API Documentation

## Overview
The AI Legal Document Assistant provides REST API endpoints for document processing and legal analysis.

## Base URL
```
http://localhost:8000
```

## Authentication
Most endpoints require user authentication. Use Django's session-based authentication or token authentication.

## Endpoints

### 1. Document Upload
**POST** `/documents/upload/`

Upload a legal document for processing.

**Request:**
- Content-Type: `multipart/form-data`
- Fields:
  - `file`: Document file (PDF, DOCX, JPG, PNG, TXT)
  - `title`: Document title (optional)

**Response:**
```json
{
    "success": true,
    "message": "File uploaded successfully",
    "redirect_url": "/document/{document_id}/"
}
```

### 2. Document Detail
**GET** `/documents/document/{id}/`

Get detailed information about a processed document.

**Response:**
```json
{
    "document": {
        "id": 1,
        "title": "Legal Contract",
        "file_type": "pdf",
        "uploaded_at": "2024-01-01T12:00:00Z",
        "is_processed": true,
        "summary": "Document summary...",
        "keywords": ["contract", "legal", "terms"],
        "constitutional_references": [...],
        "ipc_sections": [...],
        "legal_analysis": "Comprehensive analysis..."
    }
}
```

### 3. Document History
**GET** `/documents/history/`

Get list of user's uploaded documents.

**Response:**
```json
{
    "documents": [
        {
            "id": 1,
            "title": "Legal Contract",
            "file_type": "pdf",
            "uploaded_at": "2024-01-01T12:00:00Z",
            "is_processed": true
        }
    ]
}
```

### 4. Document Download
**GET** `/documents/download/{id}/{format}/`

Download processed document in specified format.

**Parameters:**
- `id`: Document ID
- `format`: `pdf` or `docx`

**Response:**
- File download (PDF or DOCX)

### 5. Legal Search API
**POST** `/legal/api/search/`

Search for legal references using semantic search.

**Request:**
```json
{
    "query": "contract law and liability"
}
```

**Response:**
```json
{
    "constitution": [
        {
            "text": "Article text...",
            "article": "Article 19",
            "score": 0.85
        }
    ],
    "ipc": [
        {
            "section": "420",
            "description": "Cheating and dishonestly inducing delivery of property",
            "punishment": "Imprisonment...",
            "score": 0.72
        }
    ]
}
```

## Error Responses

### 400 Bad Request
```json
{
    "error": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
    "error": "Authentication required"
}
```

### 404 Not Found
```json
{
    "error": "Document not found"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error"
}
```

## Rate Limiting
- Upload: 10 requests per minute per user
- Search: 60 requests per minute per user
- Download: 30 requests per minute per user

## File Upload Limits
- Maximum file size: 10MB
- Allowed file types: PDF, DOCX, JPG, PNG, TXT
- Maximum files per user: 100

## Response Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `413`: Payload Too Large
- `500`: Internal Server Error

## Example Usage

### Upload Document
```bash
curl -X POST \
  http://localhost:8000/documents/upload/ \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@document.pdf' \
  -F 'title=Legal Contract'
```

### Search Legal References
```bash
curl -X POST \
  http://localhost:8000/legal/api/search/ \
  -H 'Content-Type: application/json' \
  -d '{"query": "contract law and liability"}'
```

### Download Document
```bash
curl -X GET \
  http://localhost:8000/documents/download/1/pdf/ \
  --output document_analysis.pdf
```

## SDK Examples

### Python
```python
import requests

# Upload document
files = {'file': open('document.pdf', 'rb')}
data = {'title': 'Legal Contract'}
response = requests.post('http://localhost:8000/documents/upload/', files=files, data=data)

# Search legal references
search_data = {'query': 'contract law and liability'}
response = requests.post('http://localhost:8000/legal/api/search/', json=search_data)
```

### JavaScript
```javascript
// Upload document
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('title', 'Legal Contract');

fetch('http://localhost:8000/documents/upload/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));

// Search legal references
fetch('http://localhost:8000/legal/api/search/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({query: 'contract law and liability'})
})
.then(response => response.json())
.then(data => console.log(data));
```

## Support
For API support and questions, contact: support@ailegalassistant.com




