from passlib.context import CryptContext

pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto") #codigo para establecer el modelo de hasheo del password

def hash(password: str): #hashea la contraseña para enviarla a la base de datos
	return pwd_context.hash(password)

def verify(plain_password, hashed_password): #verifica que la contraseña insertada en el login por el usuario sea igual a la contraseña hasheada en la BD
	return pwd_context.verify(plain_password,hashed_password)