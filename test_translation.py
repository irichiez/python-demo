"""Comprehensive tests for the translation service."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from openai import APIError, RateLimitError, APIConnectionError
from main import app
from service import TranslationService

client = TestClient(app)


class TestTranslationEndpoint:
    """Test cases for the translation endpoint."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "status" in data
        assert data["status"] == "running"
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    @patch('service.translation_service.translate', new_callable=AsyncMock)
    def test_translate_success_french(self, mock_translate):
        """Test successful translation to French."""
        mock_translate.return_value = "Bonjour, comment allez-vous?"
        
        response = client.get(
            "/api/v1/translate",
            params={"message": "Hello, how are you?", "language": "french"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["original_message"] == "Hello, how are you?"
        assert data["translated_message"] == "Bonjour, comment allez-vous?"
        assert data["target_language"] == "french"
    
    @patch('service.translation_service.translate', new_callable=AsyncMock)
    def test_translate_success_spanish(self, mock_translate):
        """Test successful translation to Spanish."""
        mock_translate.return_value = "Hola, ¿cómo estás?"
        
        response = client.get(
            "/api/v1/translate",
            params={"message": "Hello, how are you?", "language": "spanish"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["target_language"] == "spanish"
        assert "Hola" in data["translated_message"]
    
    @patch('service.translation_service.translate', new_callable=AsyncMock)
    def test_translate_success_italian(self, mock_translate):
        """Test successful translation to Italian."""
        mock_translate.return_value = "Ciao, come stai?"
        
        response = client.get(
            "/api/v1/translate",
            params={"message": "Hello, how are you?", "language": "italian"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["target_language"] == "italian"
    
    @patch('service.translation_service.translate', new_callable=AsyncMock)
    def test_translate_success_portuguese(self, mock_translate):
        """Test successful translation to Portuguese."""
        mock_translate.return_value = "Olá, como você está?"
        
        response = client.get(
            "/api/v1/translate",
            params={"message": "Hello, how are you?", "language": "portuguese"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["target_language"] == "portuguese"
    
    @patch('service.translation_service.translate', new_callable=AsyncMock)
    def test_translate_success_romanian(self, mock_translate):
        """Test successful translation to Romanian."""
        mock_translate.return_value = "Bună, ce mai faci?"
        
        response = client.get(
            "/api/v1/translate",
            params={"message": "Hello, how are you?", "language": "romanian"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["target_language"] == "romanian"
    
    def test_translate_missing_message(self):
        """Test translation with missing message parameter."""
        response = client.get(
            "/api/v1/translate",
            params={"language": "french"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_translate_missing_language(self):
        """Test translation with missing language parameter."""
        response = client.get(
            "/api/v1/translate",
            params={"message": "Hello"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_translate_empty_message(self):
        """Test translation with empty message."""
        response = client.get(
            "/api/v1/translate",
            params={"message": "", "language": "french"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_translate_invalid_language(self):
        """Test translation with invalid language."""
        response = client.get(
            "/api/v1/translate",
            params={"message": "Hello", "language": "german"}
        )
        
        assert response.status_code == 422  # Validation error
    
    @patch('service.translation_service.translate', new_callable=AsyncMock)
    def test_translate_value_error(self, mock_translate):
        """Test handling of ValueError from service."""
        mock_translate.side_effect = ValueError("Message cannot be empty")
        
        response = client.get(
            "/api/v1/translate",
            params={"message": "   ", "language": "french"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data["detail"]
    
    @patch('service.translation_service.translate', new_callable=AsyncMock)
    def test_translate_rate_limit_error(self, mock_translate):
        """Test handling of rate limit error."""
        mock_translate.side_effect = RateLimitError(
            message="Rate limit exceeded",
            response=Mock(status_code=429),
            body=None
        )
        
        response = client.get(
            "/api/v1/translate",
            params={"message": "Hello", "language": "french"}
        )
        
        assert response.status_code == 500
    
    @patch('service.translation_service.translate', new_callable=AsyncMock)
    def test_translate_api_error(self, mock_translate):
        """Test handling of API error."""
        mock_translate.side_effect = APIError(
            message="API error",
            response=Mock(status_code=500),
            body=None
        )
        
        response = client.get(
            "/api/v1/translate",
            params={"message": "Hello", "language": "french"}
        )
        
        assert response.status_code == 500
    
    @patch('service.translation_service.translate', new_callable=AsyncMock)
    def test_translate_connection_error(self, mock_translate):
        """Test handling of connection error."""
        mock_translate.side_effect = APIConnectionError(
            message="Connection failed",
            request=Mock()
        )
        
        response = client.get(
            "/api/v1/translate",
            params={"message": "Hello", "language": "french"}
        )
        
        assert response.status_code == 500
    
    def test_translate_long_message(self):
        """Test translation with a long message."""
        long_message = "This is a very long message. " * 50
        
        with patch('service.translation_service.translate', new_callable=AsyncMock) as mock_translate:
            mock_translate.return_value = "Translated long message"
            
            response = client.get(
                "/api/v1/translate",
                params={"message": long_message, "language": "french"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert len(data["original_message"]) > 100


class TestTranslationService:
    """Test cases for the TranslationService class."""
    
    @pytest.fixture
    def service(self):
        """Create a TranslationService instance for testing."""
        with patch('service.OpenAI'):
            return TranslationService()
    
    @pytest.mark.asyncio
    async def test_translate_empty_message(self, service):
        """Test translation with empty message raises ValueError."""
        with pytest.raises(ValueError, match="Message cannot be empty"):
            await service.translate("", "french")
    
    @pytest.mark.asyncio
    async def test_translate_whitespace_only(self, service):
        """Test translation with whitespace-only message raises ValueError."""
        with pytest.raises(ValueError, match="Message cannot be empty"):
            await service.translate("   ", "french")
    
    @pytest.mark.asyncio
    async def test_translate_invalid_language(self, service):
        """Test translation with invalid language raises ValueError."""
        with pytest.raises(ValueError):
            await service.translate("Hello", "german")
    
    @pytest.mark.asyncio
    async def test_translate_success(self, service):
        """Test successful translation."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Bonjour"
        
        # Mock the synchronous OpenAI call that will be run in thread pool
        service.client.chat.completions.create = Mock(return_value=mock_response)
        
        result = await service.translate("Hello", "french")
        assert result == "Bonjour"
        assert service.client.chat.completions.create.called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

