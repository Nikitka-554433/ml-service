from datetime import datetime, timedelta
from jose import jwt
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from database import get_db
from models_orm.user_orm import UserORM, UserRole

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_user_by_username(username: str):
    """
    Получает пользователя из базы по username
    """
    db: Session = get_db()
    user = db.query(User).filter(User.username == username).first()
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет пароль: plain_password против хэшированного
    """
    return bcrypt.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Создаёт JWT токен с временем жизни expires_delta
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_user(db: Session, username: str, email: str, password: str, role: UserRole = UserRole.user):
    user = UserORM(
        username=username,
        email=email,
        password_hash=bcrypt.hash(password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session):
    """
    Возвращает список всех пользователей
    """
    return db.query(UserORM).all()

