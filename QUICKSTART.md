# Smart Election Assistant - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend (Terminal 1)
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend ready at:** http://localhost:8000

### Frontend (Terminal 2)
```bash
cd frontend
npm install
npm start
```

**Frontend ready at:** http://localhost:3000

---

## 📝 Configuration

### Add API Keys (Optional)
Edit `backend/.env`:
```
GEMINI_API_KEY=your-key-here
GOOGLE_MAPS_API_KEY=your-key-here
```

Without keys, the app uses smart fallback responses.

---

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 📚 API Documentation

**Interactive Docs**: http://localhost:8000/docs

### Key Endpoints
- `POST /api/chat/` - Chat with AI
- `GET /api/steps` - Voting steps
- `GET /api/timeline` - Election timeline
- `GET /api/faq` - Frequently asked questions
- `GET /api/first-time-voter-guide` - First-timer guide

---

## 🔧 Troubleshooting

**Port already in use?**
```bash
# Windows: Kill process on port
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

**Import errors?**
```bash
# Backend
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

**Frontend won't connect?**
- Check `.env`: `REACT_APP_API_URL=http://localhost:8000/api`
- Restart frontend: `npm start`

---

## 📖 More Help

See `README.md` for detailed setup, deployment, and feature documentation.

---

## 💡 Features

✅ Interactive AI Chatbot (Google Gemini)
✅ Voting Process Steps
✅ Election Timeline
✅ FAQ System
✅ First-Time Voter Guide
✅ Multilingual Support (EN, HI, MR)
✅ Accessibility Features
✅ Mobile Responsive
✅ No Political Bias
✅ Production Ready

---

**Ready to help citizens understand elections! 🇮🇳**
