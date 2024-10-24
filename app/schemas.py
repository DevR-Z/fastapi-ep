from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class UserCreate(BaseModel):
	email: EmailStr
	password: str

class UserOut(BaseModel):
	id: int
	email: EmailStr
	created_at: datetime

	class Config:
		from_attributes=True

class UserLogin(BaseModel):
	email: EmailStr
	password: str

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	id: Optional[int]=None

class PostBase(BaseModel): #clase base modelo que hace referencia a la tabla en la base de datos que se obtendra del body desde postman, obliga que los requests funcionen solo si contienen sus atributos
	title: str
	content: str
	published: bool = True #valor por defecto

class PostCreate(PostBase):
	pass

class Post(PostBase):
	id: int
	created_at: datetime
	owner_id: int
	owner: UserOut # el atributo owner es de tipo UserOut, en este caso se necesita que UserOut se declare primero para que no bote error

	class Config: #al establecer un response_model, se necesita esta clase config para convertir de sqlalchemy model a pydantic model
		from_attributes=True #orm_mode = True

class PostOut(BaseModel):
	Post: Post
	votes: int

	class Config:
		from_attributes=True

class Vote(BaseModel):
	post_id: int
	dir: conint(le=1) #le: less or equal to, columna que debe ser 0 o 1->0:unvote(dislike) post,1: vote(like) post
