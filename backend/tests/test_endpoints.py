"""
Test cases for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


class TestHealthCheck:
    """Test health check endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestDataEndpoints:
    """Test data retrieval endpoints"""
    
    def test_get_steps(self, client):
        """Test get voting steps endpoint"""
        response = client.get("/api/steps")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) > 0
        assert data["data"][0]["step_number"] == 1
    
    def test_get_timeline(self, client):
        """Test get election timeline endpoint"""
        response = client.get("/api/timeline")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) > 0
        assert "Announcement" in [phase["phase"] for phase in data["data"]]
    
    def test_get_faq(self, client):
        """Test get FAQ endpoint"""
        response = client.get("/api/faq")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) > 0
        assert "question" in data["data"][0]
    
    def test_get_faq_with_language(self, client):
        """Test get FAQ endpoint with language parameter"""
        response = client.get("/api/faq?language=en")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) > 0
    
    def test_get_first_time_voter_guide(self, client):
        """Test get first-time voter guide endpoint"""
        response = client.get("/api/first-time-voter-guide")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "title" in data["data"]

    def test_get_quiz(self, client):
        """Test get quiz endpoint"""
        response = client.get("/api/quiz")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) > 0
        assert "question" in data["data"][0]
        assert "options" in data["data"][0]


class TestChatEndpoint:
    """Test chat endpoint"""
    
    def test_chat_with_valid_input(self, client):
        """Test chat with valid input"""
        payload = {
            "user_input": "How do I vote?",
            "language": "en",
            "is_first_time_voter": False
        }
        response = client.post("/api/chat/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "response" in data["data"]
    
    def test_chat_with_empty_input(self, client):
        """Test chat with empty input"""
        payload = {
            "user_input": "",
            "language": "en"
        }
        response = client.post("/api/chat/", json=payload)
        assert response.status_code == 400
    
    def test_chat_with_very_long_input(self, client):
        """Test chat with very long input"""
        payload = {
            "user_input": "a" * 2000,
            "language": "en"
        }
        response = client.post("/api/chat/", json=payload)
        assert response.status_code == 400
    
    def test_chat_with_first_time_voter_flag(self, client):
        """Test chat with first-time voter flag"""
        payload = {
            "user_input": "What do I need to know?",
            "language": "en",
            "is_first_time_voter": True
        }
        response = client.post("/api/chat/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_chat_with_invalid_language(self, client):
        """Test chat with invalid language"""
        payload = {
            "user_input": "How to vote?",
            "language": "xx"
        }
        response = client.post("/api/chat/", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_chat_intent_detection_steps(self, client):
        """Test intent detection for voting steps"""
        payload = {
            "user_input": "How to vote?",
            "language": "en"
        }
        response = client.post("/api/chat/", json=payload)
        data = response.json()
        assert response.status_code == 200
        assert data.get("intent") in ["steps", "general", "clarification"]
    
    def test_chat_with_location_query(self, client):
        """Test chat with location query"""
        payload = {
            "user_input": "Where is my polling booth?",
            "language": "en",
            "location": "Mumbai"
        }
        response = client.post("/api/chat/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_chat_with_voting_free_text_question(self, client):
        """Voting-related free text should not force clarification intent"""
        payload = {
            "user_input": "What is voting and why is it important?",
            "language": "en"
        }
        response = client.post("/api/chat/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["intent"] != "clarification"
        assert "response" in data["data"]


class TestInputValidation:
    """Test input validation"""
    
    def test_injection_attempt(self, client):
        """Test protection against injection attacks"""
        payload = {
            "user_input": "<script>alert('test')</script>",
            "language": "en"
        }
        response = client.post("/api/chat/", json=payload)
        assert response.status_code == 400
    
    def test_missing_required_field(self, client):
        """Test missing required field"""
        payload = {
            "language": "en"
        }
        response = client.post("/api/chat/", json=payload)
        assert response.status_code == 422


class TestEdgeCases:
    """Test edge cases"""
    
    def test_chat_with_special_characters(self, client):
        """Test chat with special characters"""
        payload = {
            "user_input": "क्या है EVM? What is NOTA?",
            "language": "en"
        }
        response = client.post("/api/chat/", json=payload)
        assert response.status_code == 200
    
    def test_multiple_consecutive_requests(self, client):
        """Test multiple consecutive requests"""
        payload = {
            "user_input": "How to vote?",
            "language": "en"
        }
        
        for _ in range(3):
            response = client.post("/api/chat/", json=payload)
            assert response.status_code == 200
    
    def test_chat_with_ambiguous_input(self, client):
        """Test chat with ambiguous input"""
        payload = {
            "user_input": "xyz",
            "language": "en"
        }
        response = client.post("/api/chat/", json=payload)
        # Should return success with clarification or fallback
        assert response.status_code in [200, 400]
