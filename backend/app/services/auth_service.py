import boto3
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any
from ..config import get_settings
from ..schemas.auth import UserInfo

settings = get_settings()

class AuthService:
    def __init__(self):
        self.cognito_client = boto3.client(
            'cognito-idp',
            region_name=settings.AWS_REGION
        )
        self.user_pool_id = settings.COGNITO_USER_POOL_ID
        self.client_id = settings.COGNITO_CLIENT_ID

    async def sign_up(self, email: str, password: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Sign up a new user with AWS Cognito"""
        try:
            user_attributes = [
                {'Name': 'email', 'Value': email}
            ]
            
            if name:
                user_attributes.append({'Name': 'name', 'Value': name})

            response = self.cognito_client.sign_up(
                ClientId=self.client_id,
                Username=email,
                Password=password,
                UserAttributes=user_attributes
            )
            
            return {
                'user_id': response['UserSub'],
                'email': email,
                'message': 'User created successfully. Please check your email for confirmation code.'
            }
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UsernameExistsException':
                raise ValueError('User with this email already exists')
            elif error_code == 'InvalidPasswordException':
                raise ValueError('Password does not meet requirements')
            else:
                raise ValueError(f'Sign up failed: {e.response["Error"]["Message"]}')

    async def confirm_sign_up(self, email: str, confirmation_code: str) -> bool:
        """Confirm user sign up with confirmation code"""
        try:
            self.cognito_client.confirm_sign_up(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=confirmation_code
            )
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'CodeMismatchException':
                raise ValueError('Invalid confirmation code')
            elif error_code == 'ExpiredCodeException':
                raise ValueError('Confirmation code has expired')
            else:
                raise ValueError(f'Confirmation failed: {e.response["Error"]["Message"]}')

    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in user with email and password"""
        try:
            # Try USER_PASSWORD_AUTH first (for confirmed users)
            response = self.cognito_client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                }
            )
            
            auth_result = response['AuthenticationResult']
            return {
                'access_token': auth_result['AccessToken'],
                'refresh_token': auth_result['RefreshToken'],
                'token_type': 'Bearer',
                'expires_in': auth_result['ExpiresIn']
            }
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NotAuthorizedException':
                raise ValueError('Invalid email or password')
            elif error_code == 'UserNotConfirmedException':
                raise ValueError('Please confirm your email before signing in')
            elif error_code == 'InvalidParameterException':
                # Fallback to admin auth if user auth fails
                try:
                    response = self.cognito_client.admin_initiate_auth(
                        UserPoolId=self.user_pool_id,
                        ClientId=self.client_id,
                        AuthFlow='ADMIN_USER_PASSWORD_AUTH',
                        AuthParameters={
                            'USERNAME': email,
                            'PASSWORD': password
                        }
                    )
                    
                    auth_result = response['AuthenticationResult']
                    return {
                        'access_token': auth_result['AccessToken'],
                        'refresh_token': auth_result['RefreshToken'],
                        'token_type': 'Bearer',
                        'expires_in': auth_result['ExpiresIn']
                    }
                except ClientError as admin_error:
                    admin_error_code = admin_error.response['Error']['Code']
                    if admin_error_code == 'NotAuthorizedException':
                        raise ValueError('Invalid email or password')
                    else:
                        raise ValueError(f'Sign in failed: {admin_error.response["Error"]["Message"]}')
            else:
                raise ValueError(f'Sign in failed: {e.response["Error"]["Message"]}')

    async def get_user_info(self, access_token: str) -> UserInfo:
        """Get user information from access token"""
        try:
            response = self.cognito_client.get_user(
                AccessToken=access_token
            )
            
            user_attributes = {attr['Name']: attr['Value'] for attr in response['UserAttributes']}
            
            return UserInfo(
                user_id=response['Username'],
                email=user_attributes.get('email', ''),
                name=user_attributes.get('name'),
                email_verified=user_attributes.get('email_verified', 'false') == 'true'
            )
        except ClientError as e:
            raise ValueError(f'Failed to get user info: {e.response["Error"]["Message"]}')

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        try:
            response = self.cognito_client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refresh_token
                }
            )
            
            auth_result = response['AuthenticationResult']
            return {
                'access_token': auth_result['AccessToken'],
                'token_type': 'Bearer',
                'expires_in': auth_result['ExpiresIn']
            }
        except ClientError as e:
            raise ValueError(f'Token refresh failed: {e.response["Error"]["Message"]}')

    async def forgot_password(self, email: str) -> bool:
        """Initiate forgot password flow"""
        try:
            self.cognito_client.forgot_password(
                ClientId=self.client_id,
                Username=email
            )
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UserNotFoundException':
                raise ValueError('User not found')
            else:
                raise ValueError(f'Forgot password failed: {e.response["Error"]["Message"]}')

    async def confirm_forgot_password(self, email: str, confirmation_code: str, new_password: str) -> bool:
        """Confirm forgot password with new password"""
        try:
            self.cognito_client.confirm_forgot_password(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=confirmation_code,
                Password=new_password
            )
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'CodeMismatchException':
                raise ValueError('Invalid confirmation code')
            elif error_code == 'ExpiredCodeException':
                raise ValueError('Confirmation code has expired')
            else:
                raise ValueError(f'Password reset failed: {e.response["Error"]["Message"]}')

    async def sign_out(self, access_token: str) -> bool:
        """Sign out user"""
        try:
            self.cognito_client.global_sign_out(
                AccessToken=access_token
            )
            return True
        except ClientError as e:
            raise ValueError(f'Sign out failed: {e.response["Error"]["Message"]}') 