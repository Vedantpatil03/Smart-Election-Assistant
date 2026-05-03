"""
Intent detection service for user inputs
"""
from typing import Tuple, Optional
import re


class IntentDetector:
    """Detect user intent from input text"""
    
    # Intent keywords mapping
    INTENT_KEYWORDS = {
        "steps": [
            "how to vote", "steps", "voting process", "procedure",
            "what to do", "guide", "steps to vote", "voting steps",
            "process", "how do i vote", "voter guide", "voting guide",
            "booth", "polling", "vote", "vote kaise", "voting kaise"
        ],
        "timeline": [
            "timeline", "schedule", "dates", "when", "phases",
            "election timeline", "voting date", "announcement", "campaign",
            "nomination", "counting", "results", "timeline kya hai",
            "kab hoga", "election schedule"
        ],
        "faq": [
            "faq", "question", "common questions", "help", "information",
            "what is", "explain", "tell me about", "evm", "nota",
            "voter id", "registration", "documents", "eligibility"
        ],
        "first_time_voter": [
            "first time", "first timer", "new voter", "beginner",
            "first time voting", "first time voter", "new to voting",
            "explain simply", "easy explanation", "pehli bar", "naya voter"
        ],
        "location": [
            "location", "where", "polling station", "booth location",
            "near me", "nearby", "mera booth", "booth kaha",
            "my polling booth", "find booth"
        ]
    }

    INTENT_PRIORITY = [
        "first_time_voter",
        "location",
        "timeline",
        "faq",
        "steps",
    ]

    # Domain words used to identify election/voting-related free-text questions.
    DOMAIN_KEYWORDS = [
        "vote", "voting", "voter", "election", "electoral", "poll", "polling",
        "booth", "ballot", "evm", "nota", "candidate", "nomination", "campaign",
        "counting", "result", "constituency", "epic", "voter id", "registration"
    ]
    
    @classmethod
    def detect_intent(cls, user_input: str) -> Tuple[str, float]:
        """
        Detect user intent from input
        
        Args:
            user_input: User's text input
            
        Returns:
            Tuple of (intent, confidence)
        """
        user_input_lower = user_input.lower().strip().replace("-", " ")
        
        if not user_input_lower:
            return "general", 0.0
        
        best_intent = "general"
        best_confidence = 0.0

        for intent in cls.INTENT_PRIORITY:
            keywords = cls.INTENT_KEYWORDS.get(intent, [])
            score = 0
            for keyword in keywords:
                if keyword in user_input_lower:
                    score += 1
            
            if score > 0:
                confidence = min(1.0, 0.5 + (score - 1) * 0.25)
                if confidence > best_confidence:
                    best_intent = intent
                    best_confidence = confidence

        # If no specific intent matched but the query is election-domain, treat as FAQ.
        if best_confidence == 0.0 and cls._is_election_related(user_input_lower):
            return "faq", 0.4

        return best_intent, best_confidence

    @classmethod
    def _is_election_related(cls, user_input: str) -> bool:
        """Check if free-text input is about elections or voting."""
        return any(keyword in user_input for keyword in cls.DOMAIN_KEYWORDS)
    
    @classmethod
    def get_follow_up_question(cls, intent: str) -> str:
        """Get follow-up question based on intent"""
        follow_ups = {
            "general": "Do you want to know about: 1) Voting steps, 2) Election timeline, or 3) General FAQs?",
            "steps": "Would you like me to explain the complete voting process or any specific step?",
            "timeline": "Would you like details about a specific phase of the elections?",
            "faq": "Which topic would you like to know more about? (e.g., EVM, NOTA, voter registration)",
            "location": "Please provide your location or postal code to find nearby polling stations.",
            "first_time_voter": "Let me help you! Would you like to know: 1) What to do, 2) What to bring, or 3) How voting works?"
        }
        
        return follow_ups.get(intent, "How can I assist you with election information?")
    
    @classmethod
    def is_valid_input(cls, user_input: str) -> bool:
        """Validate user input"""
        if not user_input or len(user_input.strip()) == 0:
            return False
        
        if len(user_input) > 1000:
            return False
        
        # Check for common injection patterns
        dangerous_patterns = ["<script", "javascript:", "onclick", "onerror", "fetch("]
        for pattern in dangerous_patterns:
            if pattern in user_input.lower():
                return False
        
        return True
