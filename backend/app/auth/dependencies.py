from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.core.config import settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    print("\n========== AUTH DEBUG ==========")
    print("Received Token:", token)

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        print("Decoded Payload:", payload)

        email = payload.get("sub")
        role = payload.get("role")

        print("Email:", email)
        print("Role:", role)

        if email is None:
            print("❌ Token has no 'sub' claim.")
            raise credentials_exception

    except JWTError as e:
        print("❌ JWT Decode Error:", str(e))
        raise credentials_exception

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    print("Database User:", user)

    if user is None:
        print("❌ User not found in database.")
        raise credentials_exception

    print("✅ Authentication successful.")
    print("===============================\n")

    return user