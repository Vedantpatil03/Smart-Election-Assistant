"""
Test cases for services
"""
import pytest
from app.services.intent_detector import IntentDetector
from app.services.data_service import DataService
from app.services.chatbot_service import ChatbotService


class TestIntentDetector:
    """Test intent detection service"""
    
    def test_detect_steps_intent(self):
        """Test detection of steps intent"""
        inputs = [
            "How to vote?",
            "What are the voting steps?",
            "Tell me the procedure",
            "Vote kaise karte hain?"
        ]
        
        for user_input in inputs:
            intent, confidence = IntentDetector.detect_intent(user_input)
            assert intent == "steps"
            assert confidence > 0
    
    def test_detect_timeline_intent(self):
        """Test detection of timeline intent"""
        inputs = [
            "What is the election timeline?",
            "When is voting?",
            "Tell me the schedule",
            "Timeline kya hai?"
        ]
        
        for user_input in inputs:
            intent, confidence = IntentDetector.detect_intent(user_input)
            assert intent == "timeline"
            assert confidence > 0
    
    def test_detect_faq_intent(self):
        """Test detection of FAQ intent"""
        inputs = [
            "What is EVM?",
            "What is NOTA?",
            "Explain voter ID",
            "Tell me about registration"
        ]
        
        for user_input in inputs:
            intent, confidence = IntentDetector.detect_intent(user_input)
            assert intent == "faq"
            assert confidence > 0
    
    def test_detect_first_time_voter_intent(self):
        """Test detection of first-time voter intent"""
        inputs = [
            "I am a first-time voter",
            "I'm new to voting",
            "First time voting",
            "Pehli bar vote kar raha hoon"
        ]
        
        for user_input in inputs:
            intent, confidence = IntentDetector.detect_intent(user_input)
            assert intent == "first_time_voter"
            assert confidence > 0
    
    def test_detect_location_intent(self):
        """Test detection of location intent"""
        inputs = [
            "Where is my polling booth?",
            "Find my booth location",
            "Mera booth kaha hai?",
            "Polling station near me"
        ]
        
        for user_input in inputs:
            intent, confidence = IntentDetector.detect_intent(user_input)
            assert intent == "location"
            assert confidence > 0
    
    def test_empty_input(self):
        """Test empty input"""
        intent, confidence = IntentDetector.detect_intent("")
        assert intent == "general"
        assert confidence == 0.0
    
    def test_input_validation_empty(self):
        """Test input validation for empty string"""
        assert IntentDetector.is_valid_input("") == False
        assert IntentDetector.is_valid_input("   ") == False
    
    def test_input_validation_injection(self):
        """Test input validation for injection attempts"""
        dangerous_inputs = [
            "<script>alert('xss')</script>",
            "javascript:void(0)",
            "onclick='alert(1)'",
            "onerror='fetch(\"http://evil.com\")'"
        ]
        
        for user_input in dangerous_inputs:
            assert IntentDetector.is_valid_input(user_input) == False
    
    def test_input_validation_too_long(self):
        """Test input validation for too long input"""
        long_input = "a" * 2000
        assert IntentDetector.is_valid_input(long_input) == False
    
    def test_follow_up_questions(self):
        """Test follow-up question generation"""
        intents = ["steps", "timeline", "faq", "location", "first_time_voter", "general"]
        
        for intent in intents:
            question = IntentDetector.get_follow_up_question(intent)
            assert question
            assert len(question) > 0
            assert isinstance(question, str)

    def test_election_related_free_text_maps_to_faq(self):
        """Election-related free text should be answerable as FAQ intent"""
        intent, confidence = IntentDetector.detect_intent("Can you explain what voting means in India?")
        assert intent == "faq"
        assert confidence >= 0.3

    def test_non_election_gibberish_stays_general(self):
        """Non-election unrelated text should remain general intent"""
        intent, confidence = IntentDetector.detect_intent("abracadabra xyz")
        assert intent == "general"
        assert confidence == 0.0


class TestDataService:
    """Test data service"""
    
    def test_get_voting_steps(self):
        """Test getting voting steps"""
        steps = DataService.get_voting_steps()
        assert len(steps) == 6
        assert steps[0].step_number == 1
        assert steps[0].title == "Voter Registration"
        assert len(steps[0].description) > 0
    
    def test_get_election_timeline(self):
        """Test getting election timeline"""
        phases = DataService.get_election_timeline()
        assert len(phases) == 6
        assert phases[0].phase == "Announcement"
        phase_names = [p.phase for p in phases]
        assert "Voting Day" in phase_names
        assert "Counting & Results" in phase_names
    
    def test_get_first_time_voter_guide(self):
        """Test getting first-time voter guide"""
        guide = DataService.get_first_time_voter_guide()
        assert guide["title"]
        assert "sections" in guide
        assert len(guide["sections"]) > 0
        assert "common_questions" in guide
        assert len(guide["common_questions"]) > 0
    
    def test_steps_have_details(self):
        """Test that all steps have details"""
        steps = DataService.get_voting_steps()
        for step in steps:
            assert step.details
            assert len(step.details) > 0
    
    def test_timeline_phases_have_duration(self):
        """Test that all timeline phases have duration"""
        phases = DataService.get_election_timeline()
        for phase in phases:
            assert phase.duration
            assert len(phase.duration) > 0

    def test_get_quiz_questions(self):
        """Test getting quiz questions"""
        questions = DataService.get_quiz_questions()
        assert len(questions) > 0
        assert questions[0].question_id == 1
        assert len(questions[0].options) >= 2
        assert questions[0].correct_option_index >= 0


class TestChatbotServiceFallback:
    """Test fallback responses when API is unavailable"""

    def test_faq_fallback_is_informative(self):
        """FAQ fallback should return useful election info"""
        service = ChatbotService()
        response = service._get_fallback_response("faq", "en")

        assert response["source"] == "fallback"
        assert response["success"] is True
        assert "Voting is the process" in response["response"]
        assert "Please contact your election office for assistance." not in response["response"]

    def test_unknown_intent_falls_back_to_general(self):
        """Unknown intent should use general helper message"""
        service = ChatbotService()
        response = service._get_fallback_response("unknown_intent", "en")

        assert response["source"] == "fallback"
        assert response["success"] is True
        assert "I can help you understand election processes" in response["response"]

    def test_faq_fallback_changes_with_question_topic(self):
        """Different FAQ questions should produce different fallback responses"""
        service = ChatbotService()

        election_process = service._get_fallback_response(
            "faq", "en", "how election works"
        )
        eligibility = service._get_fallback_response(
            "faq", "en", "who is eligible for voting"
        )

        assert election_process["response"] != eligibility["response"]
        assert "stages" in election_process["response"].lower()
        assert "18" in eligibility["response"]
