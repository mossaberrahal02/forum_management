from fastapi import FastAPI, Depends, HTTPException
from sqlite3 import Connection
from schemas import UserCreate, UserUpdate, User
from crud import create_user, get_user, update_user, delete_user
from database import get_db

app = FastAPI()

@app.post("/users/", response_model=User)
def create_user_endpoint(user: UserCreate, conn: Connection = Depends(get_db)):
    user_id = create_user(conn, user)
    return {**user.dict(), "id": user_id}

@app.get("/users/{user_id}", response_model=User)
def read_user_endpoint(user_id: int, conn: Connection = Depends(get_db)):
    user = get_user(conn, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user_endpoint(user_id: int, user: UserUpdate, conn: Connection = Depends(get_db)):
    update_user(conn, user_id, user)
    return {**user.dict(), "id": user_id}

@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, conn: Connection = Depends(get_db)):
    delete_user(conn, user_id)
    return {"message": "User deleted"}