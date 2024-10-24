from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import models,schemas,oauth2
from ..database import get_db

router = APIRouter(
	prefix = "/posts",
	tags = ['Posts']
)

# @router.get("/",response_model=List[schemas.Post]) #List es necesario para obtener más de una instancia
@router.get("/",response_model=List[schemas.PostOut]) 
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),#requiere el user_id del el token que se ha establecido al loguearse, 
	limit: int = 10,skip: int = 0,search: Optional[str] = ""): #limit es un parametro que se añade al url, en este caso se usará para limitar la cantidad de instancias que se va a mostrar, para asignar el valor se añade en la url <url_name>?limit=<limit_number>
	# posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #offset: skipea los primeros "skip" instancias, contains(search)=like(f"%{search}%")
	posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #sql alchemy maneja join como left inner join por defecto
	return posts #fastapi serializa a json automaticamente

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post) #status_code-> establece el tipo de request,response_model->establece la basemodel que se retornará(en el return) al crear una instancia
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): #obtiene el post del body en postman, lo guarda en la variable new_post y lo transforma en una instancia de clase BaseModel PostCreate
	
	new_post = models.Post(owner_id=current_user.id,**post.dict()) #lo mismo que esto: models.Post(title=post.title,content=post.content,published=post.published), pero más efectivo en caso haya muchas columnas
	db.add(new_post) #inicia la transaccion de insercion
	db.commit() #guarda los cambios
	db.refresh(new_post)  #asigna a la variable new_post la instancia que se ha añadido como un diccionario
	return new_post

# @router.get("/{id}",response_model=schemas.Post)
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): #al enviar el post el id del url es string, por lo que se valida de esta forma
	# post = db.query(models.Post).filter(models.Post.id==id).first()
	post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
			detail = {"message":f"post with id {id} was not found"})		
	return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
	post_query = db.query(models.Post).filter(models.Post.id==id)
	post = post_query.first()

	if post== None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
			detail=f"post with id {id} not exists")
	if post.owner_id!=current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
			detail=f"Not authorized to perform request action")
	post_query.delete(synchronize_session=False)
	db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT) #al usar el metodo delete, generalmente no se espera algun mensaje devuelta

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
	post_query = db.query(models.Post).filter(models.Post.id==id)
	post = post_query.first()
	if post==None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
			detail=f"post with id {id} not exists")
	if post.owner_id!=current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
			detail=f"Not authorized to perform request action")
	post_query.update(updated_post.dict(),synchronize_session=False)
	db.commit()
	return post_query.first()