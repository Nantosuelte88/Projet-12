from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker


def create_db_connection():
    """
    Etablit une connexion à la base de données en utilisant les informations d'environnement.
    """

    # Charge les variables d'environnement à partir du fichier .env
    load_dotenv()

    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    db_url = f'mysql+mysqlconnector://{db_user}:{
        db_password}@{db_host}:{db_port}/{db_name}'

    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session
