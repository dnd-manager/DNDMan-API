import uuid
from sqlalchemy.orm import Session

from dndman_api import database
from dndman_api import schemas

from argon2 import PasswordHasher

ph = PasswordHasher()

def get_user(db: Session, user_id: int):
    """
    Returns use from database, using their ID.

    :param db: SQLAlchemy Session object
    :param user_id: The ID of the user
    :return: A user object with the users information
    """
    return db.query(database.User).filter(database.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Returns user from database, using their email.

    :param db: SQLAlchemy Session object
    :param email: The email of the user
    :return: A user object with the users information
    """
    return db.query(database.User).filter(database.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Returns a slice of all users in the database.

    :param db: SQLAlchemy Session object
    :param skip: How many users to skip
    :param limit: Maximum number of users to return
    :return: A list of users in the database
    """
    return db.query(database.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates and adds new user to the database.

    :param db: SQLAlchemy Session object
    :param user: PyDantic UserCreate Schema
    :return: A user object with the users information
    """
    # pseudo_hashed_password = user.password + "notreallyhashed"
    hashed_password = ph.hash(user.password)
    db_user = database.User(
        email=user.email, username=user.username, hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def create_user_session(db: Session, user_id: int):
    """
    Creates and adds a new session to the database

    :param db: SQLAlchemy Session object
    :param user_id: User that the session is created for
    :return: The created session ID
    """

    session_id = str(uuid.uuid4())

    db_user_session = database.UserSession(
        user_id=user_id,
        id=session_id
    )
    db.add(db_user_session)
    db.commit()
    db.refresh(db_user_session)
    return session_id

def get_user_session_by_user(db: Session, user_id: int):
    """
    Get the user session a user is in right now. Nullable
    
    :param db: SQLAlchemy Session object
    :param user_id: User that the session is created for
    :return: The user session
    """

    return db.query(database.UserSession).filter(database.UserSession.user_id == user_id).first()

def delete_user_session(db: Session, session_id: str):
    """
    Delete the user session with the given session id

    :param db: SQLAlchemy Session object
    :param user_id: The session with id that you want to delete
    """
    
    db.query(database.UserSession).filter(database.UserSession.id == session_id).delete(synchronize_session="evaluate")
    db.commit()