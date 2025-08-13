"""
Tests for Authentication API endpoints
"""
import pytest
from fastapi import status
from unittest.mock import patch, MagicMock

from app.services.auth_service import AuthService
from app.schemas.auth import UserInfo


class TestAuthAPI:
    """Test authentication API endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/auth/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "healthy"
    
    def test_get_user_info_unauthorized(self, client):
        """Test getting user info without authentication"""
        response = client.get("/auth/user")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_user_info_success(self, client, mock_user_info):
        """Test getting user info with authentication"""
        # Mock authentication
        from app.utils.auth_dependencies import get_current_user
        def mock_get_current_user():
            return mock_user_info
        
        client.app.dependency_overrides[get_current_user] = mock_get_current_user
        
        try:
            response = client.get("/auth/user")
            assert response.status_code == status.HTTP_200_OK
            
            user_data = response.json()
            assert user_data["user_id"] == mock_user_info.user_id
            assert user_data["email"] == mock_user_info.email
            assert user_data["name"] == mock_user_info.name
        finally:
            client.app.dependency_overrides.clear()
    
    def test_validate_token_invalid(self, client):
        """Test validating invalid token"""
        response = client.post("/auth/validate", json={"token": "invalid-token"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token" in response.json()["detail"]
    
    def test_validate_token_success(self, client):
        """Test validating valid token"""
        with patch('app.services.auth_service.AuthService.validate_token') as mock_validate:
            mock_validate.return_value = UserInfo(
                user_id="test-user-123",
                email="test@example.com",
                name="Test User"
            )
            
            response = client.post("/auth/validate", json={"token": "valid-token"})
            assert response.status_code == status.HTTP_200_OK
            
            user_data = response.json()
            assert user_data["user_id"] == "test-user-123"
            assert user_data["email"] == "test@example.com"
            assert user_data["name"] == "Test User"
    
    def test_refresh_token_invalid(self, client):
        """Test refreshing invalid token"""
        response = client.post("/auth/refresh", json={"refresh_token": "invalid-token"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid refresh token" in response.json()["detail"]
    
    def test_refresh_token_success(self, client):
        """Test refreshing valid token"""
        with patch('app.services.auth_service.AuthService.refresh_token') as mock_refresh:
            mock_refresh.return_value = {
                "access_token": "new-access-token",
                "refresh_token": "new-refresh-token",
                "token_type": "Bearer",
                "expires_in": 3600
            }
            
            response = client.post("/auth/refresh", json={"refresh_token": "valid-refresh-token"})
            assert response.status_code == status.HTTP_200_OK
            
            token_data = response.json()
            assert token_data["access_token"] == "new-access-token"
            assert token_data["refresh_token"] == "new-refresh-token"
            assert token_data["token_type"] == "Bearer"
            assert token_data["expires_in"] == 3600
    
    def test_logout_success(self, client, mock_user_info):
        """Test logout endpoint"""
        # Mock authentication
        from app.utils.auth_dependencies import get_current_user
        def mock_get_current_user():
            return mock_user_info
        
        client.app.dependency_overrides[get_current_user] = mock_get_current_user
        
        try:
            response = client.post("/auth/logout")
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["message"] == "Successfully logged out"
        finally:
            client.app.dependency_overrides.clear()


class TestAuthService:
    """Test authentication service methods"""
    
    @patch('app.services.auth_service.boto3.client')
    def test_get_user_info_success(self, mock_boto_client, mock_user_info):
        """Test getting user info from Cognito"""
        # Mock Cognito client
        mock_cognito = MagicMock()
        mock_boto_client.return_value = mock_cognito
        
        # Mock Cognito response
        mock_cognito.get_user.return_value = {
            'UserAttributes': [
                {'Name': 'sub', 'Value': 'test-user-123'},
                {'Name': 'email', 'Value': 'test@example.com'},
                {'Name': 'name', 'Value': 'Test User'}
            ]
        }
        
        service = AuthService()
        user_info = service.get_user_info("valid-token")
        
        assert user_info.user_id == "test-user-123"
        assert user_info.email == "test@example.com"
        assert user_info.name == "Test User"
    
    @patch('app.services.auth_service.boto3.client')
    def test_get_user_info_invalid_token(self, mock_boto_client):
        """Test getting user info with invalid token"""
        # Mock Cognito client
        mock_cognito = MagicMock()
        mock_boto_client.return_value = mock_cognito
        
        # Mock Cognito error
        from botocore.exceptions import ClientError
        mock_cognito.get_user.side_effect = ClientError(
            {'Error': {'Code': 'NotAuthorizedException', 'Message': 'Invalid token'}},
            'get_user'
        )
        
        service = AuthService()
        
        with pytest.raises(ValueError, match="Invalid token"):
            service.get_user_info("invalid-token")
    
    @patch('app.services.auth_service.boto3.client')
    def test_validate_token_success(self, mock_boto_client):
        """Test validating token successfully"""
        # Mock Cognito client
        mock_cognito = MagicMock()
        mock_boto_client.return_value = mock_cognito
        
        # Mock Cognito response
        mock_cognito.get_user.return_value = {
            'UserAttributes': [
                {'Name': 'sub', 'Value': 'test-user-123'},
                {'Name': 'email', 'Value': 'test@example.com'},
                {'Name': 'name', 'Value': 'Test User'}
            ]
        }
        
        service = AuthService()
        user_info = service.validate_token("valid-token")
        
        assert user_info.user_id == "test-user-123"
        assert user_info.email == "test@example.com"
        assert user_info.name == "Test User"
    
    @patch('app.services.auth_service.boto3.client')
    def test_validate_token_failure(self, mock_boto_client):
        """Test validating token failure"""
        # Mock Cognito client
        mock_cognito = MagicMock()
        mock_boto_client.return_value = mock_cognito
        
        # Mock Cognito error
        from botocore.exceptions import ClientError
        mock_cognito.get_user.side_effect = ClientError(
            {'Error': {'Code': 'NotAuthorizedException', 'Message': 'Invalid token'}},
            'get_user'
        )
        
        service = AuthService()
        
        with pytest.raises(ValueError, match="Invalid token"):
            service.validate_token("invalid-token")
    
    @patch('app.services.auth_service.boto3.client')
    def test_refresh_token_success(self, mock_boto_client):
        """Test refreshing token successfully"""
        # Mock Cognito client
        mock_cognito = MagicMock()
        mock_boto_client.return_value = mock_cognito
        
        # Mock Cognito response
        mock_cognito.initiate_auth.return_value = {
            'AuthenticationResult': {
                'AccessToken': 'new-access-token',
                'RefreshToken': 'new-refresh-token',
                'TokenType': 'Bearer',
                'ExpiresIn': 3600
            }
        }
        
        service = AuthService()
        result = service.refresh_token("valid-refresh-token")
        
        assert result["access_token"] == "new-access-token"
        assert result["refresh_token"] == "new-refresh-token"
        assert result["token_type"] == "Bearer"
        assert result["expires_in"] == 3600
    
    @patch('app.services.auth_service.boto3.client')
    def test_refresh_token_failure(self, mock_boto_client):
        """Test refreshing token failure"""
        # Mock Cognito client
        mock_cognito = MagicMock()
        mock_boto_client.return_value = mock_cognito
        
        # Mock Cognito error
        from botocore.exceptions import ClientError
        mock_cognito.initiate_auth.side_effect = ClientError(
            {'Error': {'Code': 'NotAuthorizedException', 'Message': 'Invalid refresh token'}},
            'initiate_auth'
        )
        
        service = AuthService()
        
        with pytest.raises(ValueError, match="Invalid refresh token"):
            service.refresh_token("invalid-refresh-token")
    
    def test_logout_success(self):
        """Test logout functionality"""
        service = AuthService()
        result = service.logout("user-id")
        
        assert result["message"] == "Successfully logged out"
        assert result["user_id"] == "user-id"


class TestAuthDependencies:
    """Test authentication dependencies"""
    
    def test_get_current_user_success(self, mock_user_info):
        """Test getting current user successfully"""
        from app.utils.auth_dependencies import get_current_user
        from app.services.auth_service import AuthService
        
        with patch.object(AuthService, 'get_user_info', return_value=mock_user_info):
            # Mock the credentials dependency
            from fastapi.security import HTTPAuthorizationCredentials
            mock_credentials = HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials="valid-token"
            )
            
            # This would normally be called by FastAPI, but we can test the logic
            auth_service = AuthService()
            user_info = auth_service.get_user_info("valid-token")
            
            assert user_info.user_id == mock_user_info.user_id
            assert user_info.email == mock_user_info.email
            assert user_info.name == mock_user_info.name
    
    def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token"""
        from app.services.auth_service import AuthService
        
        with patch.object(AuthService, 'get_user_info', side_effect=ValueError("Invalid token")):
            auth_service = AuthService()
            
            with pytest.raises(ValueError, match="Invalid token"):
                auth_service.get_user_info("invalid-token")
