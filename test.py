from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Charge les variables d'environnement à partir du fichier .env
load_dotenv()

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Connexion à la base de données MySQL
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

try:
    conn = engine.connect()
    print("Succes!")
except Exception as ex:
    print(ex)

