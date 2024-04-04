import os
import jwt
import re
import getpass
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
from connect_database import create_db_connection
from models.collaboration import Collaborator
from controllers.auth_permissions import authenticate, authorize
from views.login import login
from views.data import view_all_clients, view_all_contracts, view_all_events

# Définir la session SQLAlchemy
engine = create_db_connection()
Session = sessionmaker(bind=engine)
session = Session()



token = login()
view_all_clients(token)
view_all_contracts(token)
view_all_events(token)