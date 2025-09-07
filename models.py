from datetime import datetime
from typing import List
from pydantic import BaseModel

# class User(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     username: str = Field(index=True, unique=True)
#     hashed_password: str
#     is_active: bool = Field(default=True)
#     is_admin: bool = Field(default=False)

# class Admin(SQLModel, table=True):
#     pass

# class Auth(SQLModel, table=True):
#     pass

# class ContentTypes(SQLModel, table=True):
#     pass

# class Sessions(SQLModel, table=True):
#     pass

# class StaticFiles(SQLModel, table=True):
#     pass

class Job(BaseModel):
    job_name : str
    trigger_type : str
    next_trigger_time : datetime

class Jobs(BaseModel):
    jobs : List[Job]