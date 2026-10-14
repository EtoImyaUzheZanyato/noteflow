"""Модуль аутентификации и регистрации пользователей.

Реализует регистрацию, вход и проверку JWT-токенов.
"""

import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from .db import get_session
from .models import User

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXP_DAYS = 7


def _hash_password(password: str) -> str:
    """Хеширует пароль с использованием SHA-256 и соли.

    Args:
        password (str): Пароль в открытом виде.

    Returns:
        str: Хеш пароля в hex-формате.
    """
    salt = os.getenv("PASSWORD_SALT", "static-salt").encode()
    return hashlib.sha256(salt + password.encode()).hexdigest()


def register(email: str, password: str) -> dict:
    """Регистрирует нового пользователя.

    Args:
        email (str): Email пользователя. Должен быть уникальным.
        password (str): Пароль (минимум 6 символов).

    Returns:
        dict: Данные пользователя: ``{"id": int, "email": str}``.

    Raises:
        ValueError: Если email занят или пароль короче 6 символов.

    Examples:
        >>> user = register("student@example.com", "secret123")
        >>> user["email"]
        'student@example.com'
    """
    if len(password) < 6:
        raise ValueError("Пароль должен содержать минимум 6 символов")

    with get_session() as session:
        if session.query(User).filter_by(email=email).first():
            raise ValueError("Email уже занят")

        user = User(email=email, password_hash=_hash_password(password))
        session.add(user)
        session.flush()
        return {"id": user.id, "email": user.email}


def login(email: str, password: str) -> str:
    """Аутентифицирует пользователя и возвращает JWT-токен.

    Args:
        email (str): Email пользователя.
        password (str): Пароль в открытом виде.

    Returns:
        str: JWT-токен сроком действия 7 дней.

    Raises:
        ValueError: Если email не найден или пароль неверный.

    Examples:
        >>> token = login("student@example.com", "secret123")
        >>> token.count(".")
        2
    """
    with get_session() as session:
        user = session.query(User).filter_by(email=email).first()
        if not user or user.password_hash != _hash_password(password):
            raise ValueError("Неверный email или пароль")

        payload = {
            "sub": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(days=JWT_EXP_DAYS),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """Проверяет JWT-токен и возвращает payload.

    Args:
        token (str): JWT-токен.

    Returns:
        Optional[dict]: Payload токена или ``None``, если токен невалиден.
    """
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None