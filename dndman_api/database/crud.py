from sqlalchemy.orm import Session

from dndman_api import database
from dndman_api import schemas


def get_user(db: Session, user_id: int):
    """
    Returns use from database, using their ID.

    :param db: SQLAlchemy Session object
    :param user_id: The ID of the user
    :return: A user object with the users information
    """
    return db.query(database.User).filter(database.User.id == user_id).first()


def get_user_by_username(db: Session, email: str):
    """
    Returns user from database, using their email.

    :param db: SQLAlchemy Session object
    :param email: The email of the user
    :return: A user object with the users information
    """
    return db.query(database.User).filter(database.User.username == email).first()


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
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = database.User(
        email=user.email, username=user.username, hashed_password=fake_hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
