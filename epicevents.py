from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
from connect_database import create_db_connection
from models.collaboration import Collaborator
from controllers.auth_permissions import authenticate, authorize
from views.login import login
from views.data import view_all_clients, view_all_contracts, view_all_events
from controllers.create_update import create_new_user

# Définir la session SQLAlchemy
session = create_db_connection()


token = login()
print(token)
view_all_clients(token)
# view_all_contracts(token)
# view_all_events(token)

#create_new_user(token)

#view_all_clients(token)
