# src/auth/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # adjust if different
SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme)):
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("sub"):
            raise cred_exc
        return payload  # or load user from DB using sub
    except JWTError:
        raise cred_exc
