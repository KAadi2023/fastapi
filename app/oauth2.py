import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from . import schemas, models
from .database import SessionDep
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from .config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

# openssl rand -hex 32
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int | None = payload.get("user_id")
        if id is None:
            raise credentials_exception
        return schemas.TokenData(id=id)
    except ExpiredSignatureError:
        return None
    except InvalidTokenError:
        return None
    except Exception:
        return None
    

def get_current_user(session: SessionDep, token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    if not token_data:
        raise credentials_exception
    user = session.get(models.User, token_data.id)
    if not user:
        raise credentials_exception
    return user
    
