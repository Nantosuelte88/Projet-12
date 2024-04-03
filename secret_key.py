import os
import secrets
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Générer une clé secrète aléatoire
secret_key = secrets.token_hex(32)

# Stocker la clé secrète dans une variable d'environnement
os.environ['SECRET_KEY'] = secret_key

# Vous pouvez également ajouter la clé secrète dans votre fichier .env
with open('.env', 'a') as f:
    f.write(f"\nSECRET_KEY={secret_key}")

print("Clé secrète générée et stockée avec succès !")