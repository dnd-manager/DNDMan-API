import argon2
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from dndman_api import database, schemas
from dndman_api.database import crud, get_db
from dndman_api.schemas.schemas import UserSignedIn

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="DNDMan API")
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/alive", response_model=None)
def alive():
    """Just to check if server is alive. Returns 200 with null response body"""
    pass

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Creates a new user and adds it to the database."""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User with email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Returns a list of all users in the database."""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Gets and returns a user by ID."""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/user_sessions/signin/", response_model=schemas.UserSignedIn)
def sign_in_user(user_signin: schemas.UserSigninRequest, db: Session = Depends(get_db)):
    """Automatically creates a session and returns the session id and signed in user id if information is correct, throws error 401 if not"""
    db_user = crud.get_user_by_email(db, user_signin.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        crud.password_hasher.verify(db_user.hashed_password, user_signin.password)
        session_id = crud.create_user_session(db, db_user.id)
        return UserSignedIn(session=session_id, user=db_user.id)
    except argon2.exceptions.VerifyMismatchError:
        raise HTTPException(status_code=401, detail="Incorrect password")

@app.get("/user_sessions/user_has_session/{user_id}", response_model=bool)
def does_user_have_session(user_id: int, db: Session = Depends(get_db)):
    """Creates or gets a session for user"""
    return crud.get_user_session_by_user(db, user_id) is not None

@app.post("/user_sessions/create/{user_id}", response_model=str)
def create_user_session(user_id: int, db: Session = Depends(get_db)):
    """Creates or gets a session for user"""
    return crud.create_user_session(db, user_id)

@app.post("/user_sessions/delete/{session_id}", response_model=None)
def delete_user_session(session_id: str, db: Session = Depends(get_db)):
    """Deletes a user session with given id"""
    return crud.delete_user_session(db, session_id)