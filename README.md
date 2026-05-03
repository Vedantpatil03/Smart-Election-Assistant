# Smart Election Assistant 

## Project Overview
An AI Powered Smart Election Assistant is a comprehensive Full-stack application designed to help Indian citizens understand the election process, voting timeline, and steps in a simple, multilingual, and accessible way.

---



### Required Software
- Python 3.8+
- Node.js 16+
- npm 8+
- Git

### API Key (Get Before Running)
. **Google Gemini API Key**
   - Visit: https://makersuite.google.com/app/apikeys
   - Create a new project
   - Generate API key for Gemini API
   - Keep it safe (will be added to .env later)



---

## BACKEND SETUP (FastAPI)

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
1. Open `.env` file in the backend directory
2. Add your API keys:
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   
   ```
3. If no keys, leave blank - app will use fallback responses

### Step 5: Initialize Database
```bash
python -m app.database.db_setup
```

### Step 6: Run Backend Server
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**

**API Documentation**: http://localhost:8000/docs

---

## FRONTEND SETUP (React)

### Step 1: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Configure Environment Variables
1. Create/edit `.env` file:
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

### Step 4: Start Development Server
```bash
npm start
```

Frontend will be available at: **http://localhost:3000**

---

## TESTING

### Backend Tests (pytest)

```bash
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_endpoints.py

# Run specific test
pytest tests/test_endpoints.py::TestHealthCheck::test_root_endpoint

# Run with coverage
pytest --cov=app tests/
```

### Test Files
- `tests/conftest.py` - Test configuration and fixtures
- `tests/test_endpoints.py` - API endpoint tests
- `tests/test_services.py` - Service layer tests

### Frontend Tests (React)

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

---

## API ENDPOINTS

### Health Checks
- `GET /` - Welcome message
- `GET /health` - Health check

### Data Endpoints
- `GET /api/steps` - Get voting process steps
- `GET /api/timeline` - Get election timeline phases
- `GET /api/faq?language=en` - Get FAQs (supports en, hi, mr)
- `GET /api/first-time-voter-guide` - Get guide for first-time voters

### Chat Endpoint
- `POST /api/chat/` - Chat with AI assistant
  ```json
  {
    "user_input": "How do I vote?",
    "language": "en",
    "is_first_time_voter": false,
    "location": null
  }
  ```
- `GET /api/chat/history?limit=10` - Get chat history

---

## FEATURES

### 1. Interactive Chatbot
- Powered by Google Gemini API
- Intent detection (steps, timeline, FAQ, first-time voter)
- Fallback responses when API not available
- Simple, clear language

### 2. Voting Steps Guide
- Step-by-step process from registration to results
- Detailed explanations for each step
- First-time voter friendly

### 3. Election Timeline
- Announcement phase
- Nomination filing
- Campaign period
- Voting day
- Counting and results

### 4. FAQ System
- EVM (Electronic Voting Machine)
- NOTA (None of the Above)
- Voter eligibility
- Registration process
- Document requirements
- And more...

### 5. Multilingual Support
- English (en)
- Hindi (हिंदी - hi)
- Marathi (मराठी - mr)

### 6. First-Time Voter Mode
- Simplified explanations
- Real-life examples
- Step-by-step guidance
- Common questions answered

### 7. Accessibility Features
- High contrast support
- Keyboard navigation
- Voice-friendly responses
- Simple language
- Mobile responsive

---

## DIRECTORY STRUCTURE

```
smart-election-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Main FastAPI application
│   │   ├── config.py               # Configuration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py          # Pydantic models
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py             # Chat routes
│   │   │   └── data.py             # Data routes
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── chatbot_service.py  # Gemini integration
│   │   │   ├── intent_detector.py  # Intent detection
│   │   │   └── data_service.py     # Data retrieval
│   │   └── database/
│   │       ├── __init__.py
│   │       └── db_setup.py         # Database configuration
│   ├── tests/
│   │   ├── conftest.py             # Test configuration
│   │   ├── test_endpoints.py       # Endpoint tests
│   │   └── test_services.py        # Service tests
│   ├── .env                        # Environment variables
│   └── requirements.txt             # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.js       # Main chat component
│   │   │   ├── MessageBubble.js    # Message display
│   │   │   ├── InputBox.js         # Input field
│   │   │   ├── LoadingIndicator.js # Loading state
│   │   │   ├── StepsCard.js        # Steps display
│   │   │   ├── TimelineCard.js     # Timeline display
│   │   │   └── *.css               # Component styles
│   │   ├── services/
│   │   │   └── api.js              # API integration
│   │   ├── pages/
│   │   ├── App.js                  # Main App component
│   │   ├── index.js                # React entry point
│   │   └── index.css               # Global styles
│   ├── public/
│   │   └── index.html              # HTML template
│   ├── .env                        # Frontend config
│   └── package.json                # Node dependencies
│
└── README.md                        # This file
```

---

## SECURITY FEATURES

1. **Input Validation**
   - Max input length: 1000 characters
   - Injection attack prevention
   - XSS protection

2. **Environment Variables**
   - API keys stored in .env
   - Not committed to git
   - Default .env file with empty keys

3. **Error Handling**
   - Safe error messages
   - No sensitive data exposure
   - Proper HTTP status codes

4. **Database**
   - SQLite for lightweight data storage
   - No sensitive data stored
   - FAQ and chat history only

---

## PERFORMANCE OPTIMIZATION

1. **Caching**
   - Static responses cached
   - FAQ data in database

2. **Async Operations**
   - FastAPI async/await
   - Non-blocking API calls

3. **Frontend**
   - React component optimization
   - Lazy loading
   - Efficient re-renders

---





**npm dependencies issue:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
- Make sure backend is running on port 8000
- Check CORS_ORIGINS in backend `.env`

---

## DEPLOYMENT

### Backend Deployment (Render)

1. Create requirements.txt (done)

   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
2. Deploy using platform's CLI

### Frontend Deployment (Netlify/Vercel)

1. Build: `npm run build`
2. Set `REACT_APP_API_URL` to production backend URL
3. Deploy `build/` folder

---










---

**Happy Voting! 🇮🇳**
