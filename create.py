import sys
sys.path.append('../')
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

from connect_database import create_db_connection
from models.clients import Base
from models.collaboration import Base as CollaborationModelsBase


# Connexion à la base de données MySQL
engine = create_db_connection()
"""
try:
    conn = engine.connect()
    print("Succes!")

    # Supprimer les tables existantes
    CollaborationModelsBase.metadata.drop_all(bind=conn)
    Base.metadata.drop_all(bind=conn)

    CollaborationModelsBase.metadata.create_all(bind=conn)
    Base.metadata.create_all(bind=conn)
except Exception as ex:
    print(ex)

"""

def main():
    session = create_db_connection()

    try:
        conn = session.connection()
        print("Succes!")

        # Modifier la colonne support_id
        alter_query = text("ALTER TABLE events MODIFY support_id INT NULL")
        conn.execute(alter_query)

    except Exception as ex:
        print(ex)

    finally:
        session.close()

if __name__ == "__main__":
    main()