from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

#ESTE ARCHIVO ES NECESARIO PARA CREAR LOS MODELOS DE LA BASE DE DATOS USANDO SQLALCHEMY Y MANTENEER EL ORDEN EN EL CODIGO, EL ORDEN QUE SE AÑADE LAS TABLAS NO INTERESA EN ESTE CASO
class Post(Base):
	__tablename__ = 'post' #nombre de la tabla en la bd

	id = Column(Integer, primary_key=True,nullable=False)
	title = Column(String, nullable=False)
	content = Column(String,nullable=False)
	published = Column(Boolean,server_default='TRUE',nullable=False) #server_default establece el valor por defecto en caso no se establezca
	created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
	owner_id = Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
	owner = relationship("User") #atributo que no se añade a una base de datos, pero se relaciona directamente con la instancia de la tabla relacionada, asi que no se necesita volver a crear la tabla para crear esta columna

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True,nullable=False)
	email = Column(String, nullable=False,unique=True)
	password = Column(String, nullable=False,)
	created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
	phone_number = Column(String)

class Vote(Base):
	__tablename__ = 'vote'

	user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),primary_key=True)
	post_id=Column(Integer,ForeignKey("post.id",ondelete="CASCADE"),primary_key=True)