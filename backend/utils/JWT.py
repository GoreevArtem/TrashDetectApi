import time

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from settings.settings import settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code")

    @staticmethod
    def signJWT(user):
        payload = {
            "user_id": str(user.id),
            "expires": time.time() + settings.ACCESS_TOKEN_EXPIRES_IN * 60
        }
        access_token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return access_token

    @staticmethod
    def decodeJWT(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except:
            return {}

    def verify_jwt(self, jwtoken: str) -> bool:
        return True if self.decodeJWT(jwtoken) else False
