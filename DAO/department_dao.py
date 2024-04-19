from models.collaboration import Department


class DepartmentDAO:
    """
    DAO (Objet d'accès aux données) pour la gestion des départements.
    """

    def __init__(self, session):
        self.session = session

    def get_all_departments(self):
        departments = self.session.query(Department).all()
        return departments

    def get_department(self, department_id):
        department = self.session.query(Department).get(department_id)
        return department

    def create_department(self, department_data):
        department = Department(**department_data)
        self.session.add(department)
        self.session.commit()
        return department

    def update_department(self, department_id, department_data):
        department = self.session.query(Department).get(department_id)
        if not department:
            return None
        for key, value in department_data.items():
            if hasattr(department, key):
                setattr(department, key, value)
        self.session.commit()
        return department

    def delete_department(self, department_id):
        department = self.session.query(Department).get(department_id)
        if not department:
            return None
        self.session.delete(department)
        self.session.commit()
        return department
