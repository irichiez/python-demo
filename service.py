"""Service layer for translation with AI integration."""
import asyncio
import logging
from typing import Literal
from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError
from config import settings, LANGUAGE_MAPPING, ALLOWED_LANGUAGES

logger = logging.getLogger(__name__)


class TranslationService:
    """Service for handling translation requests using OpenAI."""
    
    def __init__(self):
        """Initialize the translation service with OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        logger.info(f"TranslationService initialized with model: {self.model}")
    
    async def translate(
        self, 
        message: str, 
        language: Literal["french", "spanish", "italian", "portuguese", "romanian"]
    ) -> str:
        """
        Translate a message from English to the specified language.
        
        Args:
            message: The English message to translate
            language: The target language for translation
            
        Returns:
            The translated message
            
        Raises:
            ValueError: If message is empty or invalid
            APIError: If OpenAI API call fails
            RateLimitError: If rate limit is exceeded
            APIConnectionError: If connection to OpenAI fails
        """
        if not message or not message.strip():
            logger.warning("Empty message provided for translation")
            raise ValueError("Message cannot be empty")
        
        target_language = LANGUAGE_MAPPING.get(language.lower())
        if not target_language:
            logger.warning(f"Invalid language provided: {language}")
            raise ValueError(f"Invalid language: {language}. Allowed values: {list(LANGUAGE_MAPPING.keys())}")
        
        logger.info(f"Translating message to {target_language}")
        
        try:
            prompt = f"Translate the following English text to {target_language}. Only return the translation, no explanations or additional text:\n\n{message}"
            
            # Run synchronous OpenAI call in thread pool to avoid blocking
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a professional translator specializing in translating English to {target_language}."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            translated_text = response.choices[0].message.content.strip()
            logger.info(f"Successfully translated message to {target_language}")
            return translated_text
            
        except RateLimitError as e:
            logger.error(f"OpenAI rate limit exceeded: {str(e)}")
            raise
        except APIConnectionError as e:
            logger.error(f"Failed to connect to OpenAI API: {str(e)}")
            raise
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during translation: {str(e)}")
            raise


# Global service instance
translation_service = TranslationService()

