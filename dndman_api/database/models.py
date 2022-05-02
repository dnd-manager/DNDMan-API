from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from dndman_api.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(String, primary_key=True, unique=True)
    user_id = Column(Integer)