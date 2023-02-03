from typing import List

import uvicorn
from fastapi import FastAPI,HTTPException
from pydantic import UUID4

from models import Role, Gender, User, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID4("57d63905-7446-4994-be07-c7281af42b81"),
        first_name="Jamila",
        last_name="Ahmed",
        gender=Gender.female,
        roles=[Role.student]
    ),
    User(
        id=UUID4("dac2bd97-d3c4-4160-85d8-fae84aa611ca"),
        first_name="Alex",
        last_name="jones",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    )
]

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def register_user(user:User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID4):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return

    raise HTTPException(
        status_code=404,
        detail=f"user with id:{user.id} does not exists"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID4):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id:{user.id} does not exists"
    )

# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8000)