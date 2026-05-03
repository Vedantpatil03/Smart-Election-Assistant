"""
Pydantic models for request/response validation
"""
from typing import Optional, List, Any
from pydantic import BaseModel, Field, validator


class ChatRequest(BaseModel):
    """Chat request model"""
    user_input: str = Field(...)
    language: str = Field(default="en")
    is_first_time_voter: bool = Field(default=False)
    location: Optional[str] = Field(default=None)
    
    @validator('language')
    def validate_language(cls, v):
        """Validate language code"""
        valid_languages = ["en", "hi", "mr"]
        if v not in valid_languages:
            raise ValueError(f"Language must be one of {valid_languages}")
        return v


class ChatResponse(BaseModel):
    """Chat response model"""
    status: str
    data: dict
    message: str
    intent: Optional[str] = None
    language: str = "en"
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": {"response": "Step 1: Register as a voter..."},
                "message": "Response generated successfully",
                "intent": "steps",
                "language": "en"
            }
        }


class Step(BaseModel):
    """Individual step model"""
    step_number: int
    title: str
    description: str
    details: Optional[str] = None


class StepsResponse(BaseModel):
    """Steps response model"""
    status: str
    data: List[Step]
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": [
                    {
                        "step_number": 1,
                        "title": "Registration",
                        "description": "Register as a voter",
                        "details": "Visit nearest election office..."
                    }
                ],
                "message": "Voting steps retrieved successfully"
            }
        }


class TimelinePhase(BaseModel):
    """Timeline phase model"""
    phase: str
    description: str
    duration: str
    details: Optional[str] = None


class TimelineResponse(BaseModel):
    """Timeline response model"""
    status: str
    data: List[TimelinePhase]
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": [
                    {
                        "phase": "Announcement",
                        "description": "Election announcement made",
                        "duration": "Date announced",
                        "details": "EC makes official announcement"
                    }
                ],
                "message": "Timeline retrieved successfully"
            }
        }


class FAQItem(BaseModel):
    """FAQ item model"""
    question: str
    answer: str
    category: str


class FAQResponse(BaseModel):
    """FAQ response model"""
    status: str
    data: List[FAQItem]
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": [
                    {
                        "question": "What is EVM?",
                        "answer": "EVM stands for Electronic Voting Machine...",
                        "category": "voting"
                    }
                ],
                "message": "FAQs retrieved successfully"
            }
        }


class QuizQuestion(BaseModel):
    """Quiz question model"""
    question_id: int
    question: str
    options: List[str]
    correct_option_index: int
    explanation: str


class QuizResponse(BaseModel):
    """Quiz response model"""
    status: str
    data: List[QuizQuestion]
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": [
                    {
                        "question_id": 1,
                        "question": "What is the minimum age to vote in India?",
                        "options": ["16", "18", "21", "25"],
                        "correct_option_index": 1,
                        "explanation": "The minimum age to vote in India is 18 years."
                    }
                ],
                "message": "Quiz questions retrieved successfully"
            }
        }


class PollingStation(BaseModel):
    """Polling station model"""
    name: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = None


class PollingStationResponse(BaseModel):
    """Polling stations response model"""
    status: str
    data: List[PollingStation]
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": [
                    {
                        "name": "Government School #1",
                        "address": "Street Name, City",
                        "latitude": 28.7041,
                        "longitude": 77.1025,
                        "distance": 0.5
                    }
                ],
                "message": "Polling stations retrieved successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = "error"
    message: str
    code: Optional[str] = None
    details: Optional[Any] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "Invalid request",
                "code": "INVALID_INPUT",
                "details": None
            }
        }


class TranslationRequest(BaseModel):
    """Translation request model"""
    text: str = Field(..., max_length=5000)
    target_language: str = Field(default="en")
    source_language: str = Field(default="en")
    
    @validator('target_language', 'source_language')
    def validate_language_code(cls, v):
        """Validate language code"""
        valid_languages = ["en", "hi", "mr"]
        if v not in valid_languages:
            raise ValueError(f"Language must be one of {valid_languages}")
        return v


class TranslationResponse(BaseModel):
    """Translation response model"""
    status: str
    translated_text: str
    source_language: str
    target_language: str
    source: str
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "translated_text": "चुनाव के चरण...",
                "source_language": "en",
                "target_language": "hi",
                "source": "gemini",
                "message": "Translation completed successfully"
            }
        }
