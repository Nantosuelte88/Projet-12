from connect_database import create_db_connection
from models.clients import Base
from models.collaboration import Base as CollaborationModelsBase


# Connexion à la base de données MySQL
engine = create_db_connection()

try:
    conn = engine.connect()
    print("Succes!")


    CollaborationModelsBase.metadata.create_all(bind=conn)
    Base.metadata.create_all(bind=conn)
except Exception as ex:
    print(ex)
