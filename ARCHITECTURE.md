# Smart Election Assistant - Architecture & Technical Design

## System Architecture

### Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                         │
│  React 18 | React Router | Axios | React Icons               │
│  Components: Chat, Timeline, Steps, FAQ, Input               │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/JSON
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                             │
│  FastAPI | CORS Middleware | Async Support                  │
│  Routes: /api/chat, /api/steps, /api/timeline, /api/faq     │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐    ┌──────────┐    ┌──────────────┐
   │  Chat   │    │   Data   │    │  Services    │
   │ Routes  │    │ Routes   │    │ Layer        │
   └────┬────┘    └────┬─────┘    └──────┬───────┘
        │              │                 │
        ▼              ▼                 ▼
   ┌─────────────────────────────────────────────┐
   │         Service Layer                       │
   │  ├─ ChatbotService (Gemini API)            │
   │  ├─ IntentDetector (NLP)                   │
   │  ├─ DataService (Election Info)           │
   │  └─ TranslationService (i18n)             │
   └─────────────────┬──────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐ ┌──────────┐ ┌──────────┐
   │ SQLite  │ │ Gemini   │ │ Maps API │
   │Database │ │   API    │ │ (Polls)  │
   └─────────┘ └──────────┘ └──────────┘
```

---

## Component Interaction Flow

### Chat Flow
```
User Input
    ↓
InputBox Component
    ↓
API Call (axios)
    ↓
FastAPI Route: /api/chat
    ↓
IntentDetector (Analyze intent)
    ↓
ChatbotService (Get Gemini response)
    ↓
Response Handler
    ↓
ChatHistory (Save to DB)
    ↓
API Response
    ↓
ChatWindow Component
    ↓
MessageBubble Display
```

### Data Retrieval Flow
```
User Clicks "View Steps"
    ↓
API Call: GET /api/steps
    ↓
DataService.get_voting_steps()
    ↓
Return Step objects
    ↓
StepsCard Component Display
```

---

## Database Schema

### FAQ Table
```sql
CREATE TABLE faqs (
    id INTEGER PRIMARY KEY,
    question VARCHAR(255) UNIQUE,
    answer TEXT,
    category VARCHAR(50),
    language VARCHAR(10),
    created_at TIMESTAMP
)
```

### Chat History Table
```sql
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY,
    user_input VARCHAR(1000),
    bot_response TEXT,
    language VARCHAR(10),
    intent VARCHAR(50),
    created_at TIMESTAMP
)
```

---

## API Response Format

### Standard Success Response
```json
{
  "status": "success",
  "data": {...},
  "message": "Operation successful",
  "intent": "steps",
  "language": "en"
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "code": "ERROR_CODE",
  "details": null
}
```

---

## Intent Detection Algorithm

```
1. Convert input to lowercase
2. For each intent category:
   - Count keyword matches
   - Calculate confidence score
3. Return highest scoring intent
4. If confidence < 0.3: Ask for clarification
5. If no match: Return "general"
```

### Intent Categories
- **steps**: How to vote, voting process
- **timeline**: Election dates, schedule
- **faq**: Common questions, explanations
- **first_time_voter**: Beginner guide
- **location**: Polling booth location
- **general**: Other queries

---

## Security Implementation

### Input Validation
```python
@validator('user_input')
- Max length: 1000 chars
- No injection patterns
- Sanitized special chars
```

### API Security
```python
- CORS enabled for localhost:3000
- Rate limiting ready
- Input sanitization
- Error handling (no stack traces)
```

### Data Protection
```python
- No password storage
- No sensitive data in logs
- SQLite (local only)
- Environment variables for secrets
```

---

## Performance Optimization

### Backend
1. **Async Operations**
   - FastAPI async/await
   - Non-blocking Gemini calls

2. **Caching**
   - In-memory FAQ cache
   - Settings cached with @lru_cache

3. **Database**
   - Indexed queries
   - Connection pooling

### Frontend
1. **Component Optimization**
   - React.memo for MessageBubble
   - useCallback for handlers
   - Lazy loading if expanded

2. **Network**
   - Axios request timeout: 30s
   - Retry logic ready

---

## Scalability Considerations

### Current (Single Instance)
- SQLite database
- Single FastAPI process
- Local frontend

### Production Scaling
```
┌─────────────────────────────────────┐
│     Load Balancer                   │
└──────────┬──────────────────────────┘
           ├─► FastAPI Instance 1
           ├─► FastAPI Instance 2
           └─► FastAPI Instance 3
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    ┌────────────────────────────────┐
    │   PostgreSQL Database          │
    │   (Redis Cache)                │
    └────────────────────────────────┘
```

---

## Testing Strategy

### Unit Tests
- Intent detection accuracy
- Data retrieval correctness
- Input validation

### Integration Tests
- API endpoint responses
- Database operations
- Service interactions

### End-to-End Tests
- Chat flow completeness
- Data display accuracy

### Coverage Targets
- Backend: >80%
- Frontend: >70%

---

## Error Handling

### Backend
```python
try:
    # Business logic
except ValidationError:
    # Return 422 with details
except APIError:
    # Return 500 with safe message
except Exception:
    # Log and return generic error
```

### Frontend
```javascript
try {
    response = await api.sendMessage(input);
    display(response);
} catch (error) {
    if (error.response?.status === 400) {
        showValidationError();
    } else {
        showGenericError();
    }
}
```

---

## Deployment Checklist

### Backend
- [ ] Set all required API keys in .env
- [ ] Update CORS_ORIGINS for production URL
- [ ] Test with pytest
- [ ] Initialize database
- [ ] Use production ASGI server (Gunicorn)
- [ ] Enable HTTPS
- [ ] Setup logging/monitoring

### Frontend
- [ ] Build: `npm run build`
- [ ] Set REACT_APP_API_URL to production backend
- [ ] Test all features
- [ ] Optimize bundle size
- [ ] Setup CDN
- [ ] Enable compression

---

## Monitoring & Logging

### Key Metrics
- API response time
- Error rate
- Chat volume
- Popular intents
- User language preference

### Logging Points
- API requests/responses
- Database queries
- API calls (Gemini)
- Errors/exceptions

---

## Future Enhancements

1. **Features**
   - Voice input/output
   - Video tutorials
   - Live polling booth finder
   - SMS support

2. **Performance**
   - Redis caching
   - Database clustering
   - CDN integration

3. **Analytics**
   - User behavior tracking
   - Query analytics
   - Performance dashboard

4. **Accessibility**
   - Screen reader optimization
   - Keyboard shortcuts
   - High contrast themes

---

**Last Updated**: April 30, 2026
**Version**: 1.0.0
