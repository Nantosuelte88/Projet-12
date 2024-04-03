from connect_database import create_db_connection
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
import bcrypt
from models.collaboration import Collaborator

engine = create_db_connection()

# Définissez la session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Définissez les informations pour créer le nouvel utilisateur
full_name = "Basile Hic"
email = "basile.hic@epic_events.com"
password = "password789"
department_id = 2

# Générez un sel (salt) aléatoire pour le hachage bcrypt
salt = bcrypt.gensalt()

# Hachez le mot de passe en utilisant bcrypt
hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

# Création d'un nouvel objet Collaborator avec les informations fournies et le mot de passe haché
new_collaborator = Collaborator(full_name=full_name, email=email, password=hashed_password, department_id=department_id)

# Ajoutez le nouvel objet Collaborator à la session SQLAlchemy et effectuez un commit
session.add(new_collaborator)
session.commit()

# Fermez la session
session.close()