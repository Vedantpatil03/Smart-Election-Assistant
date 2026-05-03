# API Testing Collection

## Using Postman or cURL

### Base URL
```
http://localhost:8000/api
```

---

## Health Check Endpoints

### 1. Root Endpoint
```
GET /
```

**Response:**
```json
{
  "status": "success",
  "message": "Welcome to Smart Election Assistant",
  "version": "1.0.0"
}
```

### 2. Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Application is running"
}
```

---

## Data Endpoints

### 3. Get Voting Steps
```
GET /api/steps
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/steps"
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "step_number": 1,
      "title": "Voter Registration",
      "description": "Register yourself as a voter",
      "details": "Visit your nearest election office..."
    }
  ],
  "message": "Voting steps retrieved successfully"
}
```

### 4. Get Election Timeline
```
GET /api/timeline
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/timeline"
```

### 5. Get FAQs
```
GET /api/faq?language=en
```

**Parameters:**
- `language` (optional): en, hi, mr (default: en)

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/faq?language=en"
```

### 6. Get First-Time Voter Guide
```
GET /api/first-time-voter-guide
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/first-time-voter-guide"
```

---

## Chat Endpoint

### 7. Send Chat Message
```
POST /api/chat/
```

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_input": "How do I vote?",
  "language": "en",
  "is_first_time_voter": false,
  "location": null
}
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "How do I vote?",
    "language": "en",
    "is_first_time_voter": false,
    "location": null
  }'
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "response": "Step 1: Register as a voter...",
    "source": "gemini",
    "success": true
  },
  "message": "Response generated successfully",
  "intent": "steps",
  "language": "en"
}
```

### 8. Chat History
```
GET /api/chat/history?limit=10
```

**Parameters:**
- `limit` (optional): Number of records to fetch (default: 10)

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/chat/history?limit=10"

### 9. Translate Text
```
POST /api/chat/translate
```

**Request Body:**
```json
{
  "text": "How to vote?",
  "target_language": "hi",
  "source_language": "en"
}
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/chat/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What are the voting steps?",
    "target_language": "hi",
    "source_language": "en"
  }'
```

**Response:**
```json
{
  "status": "success",
  "translated_text": "मतदान के चरण क्या हैं?",
  "source_language": "en",
  "target_language": "hi",
  "source": "gemini",
  "message": "Translation completed successfully"
}
```

**Note:** Translation is handled by Google Gemini API (no separate API key needed). Supported languages: English (en), Hindi (hi), Marathi (mr).

---
```

---

## Test Scenarios

### Scenario 1: First-Time Voter Inquiry
```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "I am voting for the first time, what should I do?",
    "language": "en",
    "is_first_time_voter": true
  }'
```

### Scenario 2: Hindi Language
```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "मुझे वोट कैसे देना है?",
    "language": "hi"
  }'
```

### Scenario 3: Marathi Language
```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "मला मतदान कसे करावे?",
    "language": "mr"
  }'
```

### Scenario 4: Location Query
```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Where is my polling booth?",
    "language": "en",
    "location": "Mumbai"
  }'
```

---

## Error Scenarios

### Invalid Language
```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "How to vote?",
    "language": "invalid"
  }'
```

**Response (422 Validation Error):**
```json
{
  "detail": [
    {
      "loc": ["body", "language"],
      "msg": "Language must be one of [\"en\", \"hi\", \"mr\"]",
      "type": "value_error.validator"
    }
  ]
}
```

### Missing Required Field
```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "en"
  }'
```

**Response (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "user_input"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Empty Input
```bash
curl -X POST "http://localhost:8000/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "",
    "language": "en"
  }'
```

**Response (400):**
```json
{
  "detail": "Invalid input. Please provide a valid question."
}
```

---

## Postman Collection Import

Save as `postman_collection.json`:
```json
{
  "info": {
    "name": "Smart Election Assistant API",
    "version": "1.0.0"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/health"
      }
    },
    {
      "name": "Get Steps",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/api/steps"
      }
    },
    {
      "name": "Get Timeline",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/api/timeline"
      }
    },
    {
      "name": "Get FAQs",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/api/faq?language=en"
      }
    },
    {
      "name": "Chat Message",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"user_input\": \"How do I vote?\", \"language\": \"en\"}"
        },
        "url": "{{base_url}}/api/chat/"
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    }
  ]
}
```

---

**Use these endpoints for testing and integration!**
