
from connect_database import create_db_connection
from views.view_company import view_create_company

from DAO.client_dao import ClientDAO
from DAO.company_dao import CompanyDAO

session = create_db_connection()
client_dao = ClientDAO(session)
company_dao = CompanyDAO(session)


def create_company(company_name):
    """
    Crée un nouvelle entreprise
    """
    matching_companies = company_dao.get_corresponding_company(company_name)

    if company_name:
        company_data = view_create_company(company_name, matching_companies)
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
