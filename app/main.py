#pip install fastapi[all], psycopg2, sqlalchemy, passlib[bcrypt], python-jose[cryptography], alembic
#pip freeze: muestra los paquetes instalados (en este caso dentro del ambiente virtual)
#uvicorn <file_name>:<app_name> --reload
#uvicorn <folder_name>.<file_name>:<app_name> --reload en caso el programa se encuentre dentro de una carpeta
#alembic init alembic: crea un directorio para iniciar alembic, a la vez crea alembic.ini, con alembic se puede modificar tablas, añadir columnas y relaciones, lo cual no permite hacerlo sqlalchemy
#alembic revision -m "<comentario que detalla la razon de la creación del archivo revision>": crea un revision file, en su funcion upgrade se establecerá la creacion de tablas, adición o modificacion de columnas, etc. 
#alembic current: Muestra el ultimo revision file upgradeado
#alembic heads: Muestra el ultimo revision file que se acaba de crear  
#alembic upgrade <revision_code>|head: sube los cambios establecidos en la funcion upgrade de revision file|head (revisar con el comando: alembic heads) a la base de datos, tambien crea una tabla "alembic_version" la cual guarda todas las versiones de revision file upgradeadas
#alembic downgrade <revision_code>: ejecuta la funcion downgrade del revision file y vuelve al estado del revision file del codigo establecido, tambien se puede usar: alembic downgrade -1, para retroceder una version segun el revision file, puede ser -2,-3... 
#alembic revision --autogenerate -m "<mensaje detallado>": este comando sirve para que se autogenere un revision file con las tablas o columnas faltantes que hay en la clase modelo en models.py

from fastapi import FastAPI
#from random import randrange
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine) #crea la tabla en la bd segun la clase, en caso de que ya exista no permite modificar columnas, si se quiere añadir o modificar columnas se tiene que borrar la tabla existente, ya que se ha usado alembic ya no es necesario que se suba desde sqlalchemy

app = FastAPI()

origins=["https://www.google.com"] #se añade el origen de google para hacer pul request desde la consola del navegador
app.add_middleware( #para hacer un pul desde el navegador se usa este comando: fetch('http://localhost:8000/').then(res=>res.json()).then(console.log)
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

#------------USANDO LISTA DE DICCIONARIOS COMO BD SIMULADO--------------

# my_posts = [
# 	{"title":"title of post 1","content":"content of post 1", "id":1},
# 	{"title":"favorite foods","content":"i like pizza","id":2}]

# def find_post(id):
# 	for post in my_posts:
# 		if post['id']==id:
# 			 return post

# def find_index_post(id):
# 	for i,post in enumerate(my_posts):
# 		if post['id']==id:
# 			return i

# @app.get("/posts")
# return {"data":my_posts}

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):#obtiene el campo de body enviado desde Postman, lo convierte en un diccionario y lo guarda en la variable payload
# 	print(payload)
# 	return {"new_post": f"title->{payload['title']}, content->{payload['content']}"}

# @app.post("/posts", status_code=status.HTTP_201_CREATED) #sin base de datos, usando una lista de diccionarios como base de datos simulada
# def create_posts(post: Post): #obtiene el post del body en postman, lo guarda en la variable new_post y lo transforma en una instancia de clase BaseModel Post
# 	# print(post.rating)
# 	# print(post.dict())
# 	post_dict = post.dict()
# 	post_dict['id']=randrange(0,1000000)
# 	my_posts.append(post_dict)
# 	return {"data":post_dict}

# @app.get("/posts/latest") #es necesario subir esta funcion ya que si se codea abajo del get post by id priorizará esa funcion y "latest" sera invalidado por ser string y no entero
# def get_latest_post():
# 	post = my_posts[len(my_posts)-1]
# 	return {"detail": post}

# @app.get("/posts/{id}")
# def get_post(id: int, response: Response): #al enviar el post el id del url es string, por lo que se valida de esta forma
# 	post = find_post(id)
# 	if not post:
# 		response.status_code = status.HTTP_404_NOT_FOUND
# 		return {"message":f"post with id {id} was not found"}
# 	return {"post_detail":post}

# @app.get("/posts/{id}")
# def get_post(id: int): #al enviar el post el id del url es string, por lo que se valida de esta forma
# 	post = find_post(id)
# 	if not post:
# 		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
# 			detail = {"message":f"post with id {id} was not found"})		
# 	return {"post_detail":post}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
# 	index = find_index_post(id)
# 	if index==None:
# 		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
# 			detail=f"post with id {id} not exists")
# 	my_posts.pop(index)
# 	return Response(status_code=status.HTTP_204_NO_CONTENT) #al usar el metodo delete, generalmente no se espera algun mensaje devuelta

# @app.put("/posts/{id}")
# def update_post(id:int, post: Post):
# 	index = find_index_post(id)
# 	if index==None:
# 		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
# 			detail=f"post with id {id} not exists")
# 	post_dict = post.dict()
# 	post_dict['id']= id
# 	my_posts[index]=post_dict
# 	return {"data":post_dict}


#------------USANDO BASE DE DATOS Y FASTAPY CON PSYCOPG2-----------------
# while True:
# 	try:
# 		conn = psycopg2.connect(
# 			host='localhost',database='fastapi',
# 			user='postgres',password='admin',
# 			cursor_factory=RealDictCursor)
# 		cursor = conn.cursor()
# 		print("Database connection was successfull!")
# 		break
# 	except Exception as error:
# 		print("Connection to database failed")
# 		print("Error: ",error)
# 		time.sleep(5)

# @app.get("/posts")
# def get_posts():
# 	cursor.execute("""SELECT * FROM post""")
# 	posts = cursor.fetchall()
# 	print(posts)
# 	return {"data": posts}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post): #obtiene el post del body en postman, lo guarda en la variable new_post y lo transforma en una instancia de clase BaseModel Post
# 	cursor.execute("""INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
# 					(post.title,post.content,post.published))
# 	new_post=cursor.fetchone()
# 	conn.commit()
# 	return {"data": new_post}

# @app.get("/posts/{id}")
# def get_post(id: int): #al enviar el post el id del url es string, por lo que se valida de esta forma
# 	cursor.execute("""SELECT * FROM post where id = %s""",(str(id),))
# 	post = cursor.fetchone()
# 	if not post:
# 		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
# 			detail = {"message":f"post with id {id} was not found"})		
# 	return {"post_detail":post}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
# 	cursor.execute("""DELETE FROM post where id = %s returning *""",(str(id),))
# 	deleted_post = cursor.fetchone()
# 	conn.commit()
# 	if deleted_post == None:
# 		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
# 			detail=f"post with id {id} not exists")
# 	return Response(status_code=status.HTTP_204_NO_CONTENT) #al usar el metodo delete, generalmente no se espera algun mensaje devuelta

# @app.put("/posts/{id}")
# def update_post(id:int, post: Post):
# 	cursor.execute("""UPDATE post SET title = %s, content=%s,published=%s where id=%s returning *""",
# 					(post.title,post.content,post.published,id))
# 	updated_post = cursor.fetchone()
# 	conn.commit()
# 	if update_post==None:
# 		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
# 			detail=f"post with id {id} not exists")
# 	return {"data":updated_post}

#---------------------USANDO SQLALCHEMY-----------------

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)	
app.include_router(vote.router)	

@app.get("/")
def root():
	return {"message":"¡¡Hello World!!"}