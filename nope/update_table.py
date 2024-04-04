from sqlalchemy import MetaData, Table, Column, Boolean
from connect_database import create_db_connection
from models.clients import Base
from models.collaboration import Base as CollaborationModelsBase


# Connexion à la base de données MySQL
engine = create_db_connection()

try:
    conn = engine.connect()
    print("Succes!")


    # Créez un objet MetaData avec le moteur de base de données
    metadata = MetaData(bind=engine)

    # Obtenez la table contracts existante à partir de la base de données
    contracts_table = Table('contracts', metadata, autoload=True)

    # Modifiez la colonne status pour utiliser le type Boolean
    status_column = Column('status', Boolean, default=False)
    contracts_table.c.status.alter(status_column)

    # Appliquez les modifications à la base de données
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)
except Exception as ex:
    print(ex)