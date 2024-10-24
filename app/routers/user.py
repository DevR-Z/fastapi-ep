from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from ..database import get_db

router = APIRouter(
	prefix = "/users", #añadir prefijo en las url para que no sea repetitivo
	tags = ['Users'] #para formar grupo en la documentacion de fastapi en 127.0.0.1:8000/docs
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
	hashed_password = utils.hash(user.password) #aplicar el hash(encriptación) a la contraseña
	user.password=hashed_password
	new_user = models.User(**user.dict()) 
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.id==id).first()
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exist")
	return user	