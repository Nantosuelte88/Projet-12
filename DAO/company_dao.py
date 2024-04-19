from models.clients import Company


class CompanyDAO:
    """
    DAO (Objet d'accès aux données) pour la gestion des entreprises.
    """

    def __init__(self, session):
        self.session = session

    def get_all_companys(self):
        companys = self.session.query(Company).all()
        return companys

    def get_company(self, company_id):
        company = self.session.query(Company).get(company_id)
        return company

    def get_corresponding_company(self, company_name):
        companys_names_min = self.session.query(Company).filter(
            Company.name.ilike(f"%{company_name}%")).all()
        return companys_names_min

    def get_company_by_name(self, company_name):
        company = self.session.query(Company).filter_by(
            name=company_name).first()
        return company

    def create_company(self, company_data):
        company = Company(**company_data)
        self.session.add(company)
        self.session.commit()
        return company

    def update_company(self, company_id, company_data):
        company = self.session.query(Company).get(company_id)
        if not company:
            return None
        for key, value in company_data.items():
            if hasattr(company, key):
                setattr(company, key, value)
        self.session.commit()
        return company

    def delete_company(self, company_id):
        company = self.session.query(Company).get(company_id)
        if not company:
            return None
        self.session.delete(company)
        self.session.commit()
        return company
