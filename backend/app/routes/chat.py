"""
Chat routes for the election assistant
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.schemas import ChatRequest, ChatResponse, TranslationRequest, TranslationResponse
from app.services.chatbot_service import ChatbotService
from app.services.intent_detector import IntentDetector
from app.database.db_setup import get_db, ChatHistory

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    if not IntentDetector.is_valid_input(request.user_input):
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Please provide a valid question."
        )

    intent, confidence = IntentDetector.detect_intent(request.user_input)

    if confidence < 0.3:
        follow_up = IntentDetector.get_follow_up_question("general")
        return ChatResponse(
            status="success",
            data={"response": follow_up},
            message="Please clarify your question",
            intent="clarification",
            language=request.language,
        )

    chatbot = ChatbotService()

    try:
        response_data = await chatbot.get_response(
            user_input=request.user_input,
            intent=intent,
            language=request.language,
            is_first_time_voter=request.is_first_time_voter,
        )

        chat_record = ChatHistory(
            user_input=request.user_input,
            bot_response=response_data.get("response", ""),
            language=request.language,
            intent=intent,
        )
        db.add(chat_record)
        db.commit()

        return ChatResponse(
            status="success",
            data=response_data,
            message="Response generated successfully",
            intent=intent,
            language=request.language,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@router.get("/history", response_model=list)
async def get_chat_history(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    try:
        history = db.query(ChatHistory).order_by(
            ChatHistory.created_at.desc()
        ).limit(limit).all()

        return [
            {
                "user_input": record.user_input,
                "bot_response": record.bot_response,
                "intent": record.intent,
                "language": record.language,
                "created_at": record.created_at.isoformat(),
            }
            for record in history
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving history: {str(e)}"
        )


@router.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Text to translate cannot be empty"
        )

    chatbot = ChatbotService()

    try:
        translation_data = await chatbot.translate_text(
            text=request.text,
            target_language=request.target_language,
            source_language=request.source_language,
        )

        return TranslationResponse(
            status="success",
            translated_text=translation_data.get("translated_text", ""),
            source_language=request.source_language,
            target_language=request.target_language,
            source=translation_data.get("source", "fallback"),
            message="Translation completed successfully",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing translation: {str(e)}"
        )
