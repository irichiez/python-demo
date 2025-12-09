"""REST controller for translation endpoints."""
import logging
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Literal
from service import translation_service
from config import ALLOWED_LANGUAGES

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["translation"])


class TranslationResponse(BaseModel):
    """Response model for translation endpoint."""
    original_message: str = Field(..., description="The original English message")
    translated_message: str = Field(..., description="The translated message")
    target_language: str = Field(..., description="The target language")
    
    class Config:
        json_schema_extra = {
            "example": {
                "original_message": "Hello, how are you?",
                "translated_message": "Bonjour, comment allez-vous?",
                "target_language": "french"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: str = Field(..., description="Detailed error information")


@router.get(
    "/translate",
    response_model=TranslationResponse,
    responses={
        200: {"description": "Translation successful"},
        400: {"description": "Bad request - invalid parameters", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse},
        503: {"description": "Service unavailable - API error", "model": ErrorResponse}
    },
    summary="Translate English message to target language",
    description="Translates an English message to one of the supported languages using OpenAI"
)
async def translate_message(
    message: str = Query(..., description="The English message to translate", min_length=1),
    language: ALLOWED_LANGUAGES = Query(..., description="Target language for translation")
) -> TranslationResponse:
    """
    Translate an English message to the specified target language.
    
    Args:
        message: The English message to translate (required)
        language: Target language - one of: french, spanish, italian, portuguese, romanian (required)
        
    Returns:
        TranslationResponse with original message, translated message, and target language
        
    Raises:
        HTTPException: If translation fails or parameters are invalid
    """
    logger.info(f"Received translation request: message='{message[:50]}...', language={language}")
    
    try:
        translated_text = await translation_service.translate(message, language)
        
        response = TranslationResponse(
            original_message=message,
            translated_message=translated_text,
            target_language=language
        )
        
        logger.info(f"Translation successful for language: {language}")
        return response
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid request parameters",
                "detail": str(e)
            }
        )
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Translation service error",
                "detail": str(e)
            }
        )

