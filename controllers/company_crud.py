
from connect_database import create_db_connection
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from models.collaboration import Collaborator, Department
from models.clients import Client, Contract, Event
from datetime import datetime, timedelta, timezone
from utils.decorators import department_permission_required
from views.view_company import view_create_company

from DAO.client_dao import ClientDAO
from DAO.company_dao import CompanyDAO

session = create_db_connection()
# Création de l'instance du DAO Client
client_dao = ClientDAO(session)
company_dao = CompanyDAO(session)


def create_company(company_name):
    if company_name:
        company_data = view_create_company(company_name)
        print(company_data)
        
        # Création de l'entreprise
        new_company_data = {
            'name': company_data[0],
            'phone_number': company_data[1],
            'address': company_data[2],
            'industry': company_data[3]
        } 
        new_company = company_dao.create_company(new_company_data)
        if new_company:
            print("Nouvelle entreprise crée")
        else:
            print("Une erreur s\'est produite")
        

