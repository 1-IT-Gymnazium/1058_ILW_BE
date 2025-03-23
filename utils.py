from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer
from config import get_settings


class UnauthorizedException(HTTPException):
    """Exception raised when authentication token is invalid or lacks necessary permissions."""

    def __init__(self, detail: str, **kwargs):
        """
        Initializes UnauthorizedException.

        :param detail: Detailed message explaining why the exception was raised.
        :param kwargs: Additional keyword arguments passed to HTTPException.
        """
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    """Exception raised when authentication token is missing or not provided."""

    def __init__(self):
        """Initializes UnauthenticatedException with a default message."""
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires authentication"
        )


class VerifyToken:
    """Class responsible for verifying JWT tokens using PyJWT and JWKS."""

    def __init__(self):
        """Initializes VerifyToken by configuring JWKS client."""
        self.config = get_settings()

        # Fetch JWKS from a URL provided by Auth0 domain
        jwks_url = f'https://{self.config.auth0_domain}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())
    ):
        """
        Verifies JWT token and returns the payload if valid.

        :param security_scopes: Security scopes required for accessing certain endpoints.
        :param token: JWT token extracted from the HTTP Authorization header.
        :return: Decoded JWT payload if token is valid.

        :raises UnauthenticatedException: When no token is provided.
        :raises UnauthorizedException: When token verification fails or decoding errors occur.
        """
        if token is None:
            raise UnauthenticatedException()

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token.credentials
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=self.config.auth0_algorithms,
                audience=self.config.auth0_api_audience,
                issuer=self.config.auth0_issuer,
            )
        except Exception as error:
            raise UnauthorizedException(str(error))

        return payload