from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..config import settings
from .. import demo_data

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def create_access_token(subject: str, role: str, full_name: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "role": role, "name": full_name, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])


def authenticate_user(db: Session | None, username: str, password: str) -> dict | None:
    if settings.demo_mode:
        row = demo_data.USERS.get(username)
        if not row or not row["is_active"]:
            return None
        if not verify_password(password, row["password_hash"]):
            return None
        return dict(row)

    assert db is not None
    row = db.execute(
        text(
            """
            SELECT u.username, u.full_name, u.password_hash, u.is_active, r.role_code
            FROM app_auth.users u
            JOIN app_auth.roles r ON r.role_id = u.role_id
            WHERE u.username = :u
            """
        ),
        {"u": username},
    ).mappings().first()
    if not row or not row["is_active"]:
        return None
    if not verify_password(password, row["password_hash"]):
        return None
    return dict(row)


def ensure_demo_passwords(db: Session) -> None:
    if settings.demo_mode:
        return
    known = hash_password("ChangeMe123!")
    db.execute(
        text("UPDATE app_auth.users SET password_hash = :h WHERE username = ANY(:names)"),
        {"h": known, "names": ["ceo", "risk", "report", "auditor", "admin"]},
    )
    db.commit()
