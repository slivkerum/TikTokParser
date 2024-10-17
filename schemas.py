from pydantic import BaseModel
from typing import Optional, List


class UserResponseSchema(BaseModel):
    username: Optional[str] = None
    followers_count: Optional[str] = None
    following_count: Optional[str] = None
    likes: Optional[str] = None


class UserDataSchema(BaseModel):
    username: Optional[str] = None
    user_url: Optional[str] = None
    comment: Optional[str] = None


class CommentResponseSchema(BaseModel):
    video_id: Optional[str] = None
    video_name: Optional[str] = None
    users: List[UserDataSchema] = []
