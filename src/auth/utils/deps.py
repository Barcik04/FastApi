from uuid import UUID
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from src.auth.utils.consts import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
bearer_scheme = HTTPBearer()


def get_current_user(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_current_user_id(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> UUID:
    payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    return UUID(str(payload["sub"]))
