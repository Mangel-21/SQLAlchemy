from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear una instancia de la clase Base para definir las clases de la base de datos
Base = declarative_base()

# Definición de la clase User (Tabla principal)
class User(Base):
    __tablename__ = 'users'  # Nombre de la tabla en la base de datos

    # Definición de las columnas de la tabla
    id = Column(Integer, primary_key=True)  # Clave primaria
    name = Column(String, nullable=False)  # Nombre del usuario
    age = Column(Integer, nullable=False)  # Edad del usuario

    # Relación uno a muchos con la tabla 'Post'
    posts = relationship('Post', back_populates='author')

    def __repr__(self):
        return f"<User(name={self.name}, age={self.age})>"

# Definición de la clase Post (Tabla secundaria con relación a 'User')
class Post(Base):
    __tablename__ = 'posts'  # Nombre de la tabla en la base de datos

    # Definición de las columnas de la tabla
    id = Column(Integer, primary_key=True)  # Clave primaria
    title = Column(String, nullable=False)  # Título del post
    content = Column(String, nullable=False)  # Contenido del post
    user_id = Column(Integer, ForeignKey('users.id'))  # Llave foránea a 'users.id'

    # Relación inversa con la tabla 'User'
    author = relationship('User', back_populates='posts')

    def __repr__(self):
        return f"<Post(title={self.title}, content={self.content})>"

# Crear una conexión a la base de datos PostgreSQL llamada 'pythonORM'
engine = create_engine('postgresql://giardel:12345@localhost/pythonORM')

# Crear todas las tablas definidas (en este caso, las tablas 'users' y 'posts') en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Crear nuevos objetos de la clase User para agregar a la base de datos
new_user = User(name="Alice", age=30)
session.add(new_user)
session.commit()  # Persistir el objeto 'User'

# Crear nuevos objetos de la clase Post relacionados con el usuario creado
new_post1 = Post(title="Primer Post de Alice", content="Contenido del primer post", user_id=new_user.id)
new_post2 = Post(title="Segundo Post de Alice", content="Contenido del segundo post", user_id=new_user.id)

# Añadir los posts a la sesión y persistir
session.add(new_post1)
session.add(new_post2)
session.commit()

# Obtener todos los usuarios (consulta simple)
users = session.query(User).all()
print("Usuarios en la base de datos:")
for user in users:
    print(user)

# Obtener un único registro por su id
user = session.query(User).filter_by(id=1).first()
print(f"\nUsuario con ID 1: {user}")

# Obtener todos los posts de un usuario específico
user_posts = session.query(Post).filter_by(user_id=new_user.id).all()
print(f"\nPosts de {new_user.name}:")
for post in user_posts:
    print(post)

# Actualizar datos de un usuario
user_to_update = session.query(User).filter_by(name="Alice").first()
if user_to_update:
    user_to_update.age = 31  # Actualizando la edad
    session.commit()
    print(f"\nUsuario actualizado: {user_to_update}")

# Eliminar un post
post_to_delete = session.query(Post).filter_by(title="Primer Post de Alice").first()
if post_to_delete:
    session.delete(post_to_delete)  # Eliminar el post
    session.commit()
    print(f"\nPost eliminado: {post_to_delete}")

# Hacer un JOIN entre tablas 'users' y 'posts' para obtener los posts de un usuario
join_query = session.query(User, Post).join(Post, User.id == Post.user_id).all()
print("\nUsuarios con sus posts:")
for user, post in join_query:
    print(f"Usuario: {user.name}, Post: {post.title}")

# Cerrar la sesión cuando ya no sea necesaria
session.close()
