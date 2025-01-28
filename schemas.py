from pydantic import BaseModel, Field, EmailStr, ConfigDict

from fastapi import FastAPI

app = FastAPI()

data = {
    "email": "abc@mail.ru",
    "bio": "Я пирожок вкусный",
    "age": 12,

}

data_wo_age = {
    "email": "abc@mail.ru",
    "bio": "Я пирожок вкусный",
}


class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=100)

    model_config = ConfigDict(extra="forbid")


users = []


@app.post('/users')
def add_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "msg": "User успешно добавлен"}


@app.get('/users')
def get_users() -> list[UserSchema]:
    return users

class UserAgeSchema(UserSchema):
    age: int = Field(ge=0, le=130)


# user_wo_age = UserSchema(**data_wo_age)
# user = UserAgeSchema(**data)
# print(repr(user))
# print(repr(user_wo_age))
