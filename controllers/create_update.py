
from connect_database import create_db_connection
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from models.collaboration import Collaborator, Department
from models.clients import Client, Contract, Event
from datetime import datetime, timedelta, timezone
from utils.decorators import department_permission_required
from views.create_update_data import view_create_client
from utils.get_object import get_id_by_token

session = create_db_connection()


# si commercial
@department_permission_required(3)
def create_new_client(token):

    print("Dans fonction create_new_user du controller")
    info_client = view_create_client()
    print(info_client)
    if info_client:

        creation_date = datetime.now(timezone.utc)
        last_contact_date = None
        commercial_id = get_id_by_token(token)
        if info_client[3]:
            # fonction pour verifier les entreprises existantes
            company_id = None
        else:
            company_id = None

        # Créez une instance du client avec les valeurs spécifiées
        new_client = Client(
            full_name=info_client[0],
            email=info_client[1],
            phone_number=info_client[2],
            creation_date=creation_date,
            last_contact_date=last_contact_date,
            commercial_id=commercial_id,
            company_name=info_client[3],
            company_id=company_id
        )

        print(new_client)
        # Ajoutez le nouveau client à la session
        session.add(new_client)
        session.commit()
