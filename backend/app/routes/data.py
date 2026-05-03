"""
Data routes for election information
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.schemas import (
    StepsResponse, TimelineResponse, FAQResponse, QuizResponse, Step, TimelinePhase, FAQItem
)
from app.services.data_service import DataService
from app.database.db_setup import get_db, FAQ

router = APIRouter(prefix="/api", tags=["data"])


@router.get("/steps", response_model=StepsResponse)
async def get_voting_steps():
    """
    Get voting process steps
    
    Returns:
        List of voting steps
    """
    try:
        steps = DataService.get_voting_steps()
        return StepsResponse(
            status="success",
            data=steps,
            message="Voting steps retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving steps: {str(e)}"
        )


@router.get("/timeline", response_model=TimelineResponse)
async def get_election_timeline():
    """
    Get election timeline and phases
    
    Returns:
        List of election phases and timeline
    """
    try:
        phases = DataService.get_election_timeline()
        return TimelineResponse(
            status="success",
            data=phases,
            message="Election timeline retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving timeline: {str(e)}"
        )


@router.get("/faq", response_model=FAQResponse)
async def get_faqs(language: str = "en", db: Session = Depends(get_db)):
    """
    Get frequently asked questions
    
    Args:
        language: Language code (en, hi, mr)
        db: Database session
        
    Returns:
        List of FAQs
    """
    try:
        # Try to get from database first
        faqs = db.query(FAQ).filter(FAQ.language == language).all()
        
        if not faqs:
            # Fallback to static content if the database is empty in this environment
            faq_items = DataService.get_faqs(language)
            return FAQResponse(
                status="success",
                data=faq_items,
                message="FAQs retrieved successfully"
            )
        
        faq_items = [
            FAQItem(
                question=faq.question,
                answer=faq.answer,
                category=faq.category
            )
            for faq in faqs
        ]
        
        return FAQResponse(
            status="success",
            data=faq_items,
            message="FAQs retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving FAQs: {str(e)}"
        )


@router.get("/first-time-voter-guide")
async def get_first_time_voter_guide():
    """
    Get first-time voter guide
    
    Returns:
        Comprehensive guide for first-time voters
    """
    try:
        guide = DataService.get_first_time_voter_guide()
        return {
            "status": "success",
            "data": guide,
            "message": "First-time voter guide retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving guide: {str(e)}"
        )


@router.get("/quiz", response_model=QuizResponse)
async def get_quiz(language: str = "en"):
    """
    Get election awareness quiz questions.

    Args:
        language: Language code (en, hi, mr)

    Returns:
        List of quiz questions
    """
    try:
        questions = DataService.get_quiz_questions(language)
        return QuizResponse(
            status="success",
            data=questions,
            message="Quiz questions retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving quiz: {str(e)}"
        )


@router.get("/")
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Welcome message
    """
    return {
        "status": "success",
        "message": "Smart Election Assistant API is running",
        "version": "1.0.0"
    }
