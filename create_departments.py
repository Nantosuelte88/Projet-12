from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker
from models.collaboration import Department

engine = create_db_connection()

# Création d'une session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Création des départements
departements = ['support', 'gestion', 'commercial']

for dept in departements:
    department = Department(name=dept)
    session.add(department)

# Valider les modifications et fermer la session
session.commit()
session.close()