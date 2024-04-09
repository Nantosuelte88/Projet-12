import jwt
import os
from models.clients import Client, Contract, Event
from models.collaboration import Collaborator, Department
from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker

from connect_database import create_db_connection
from sqlalchemy.orm import sessionmaker


class DepartmentDAO:
    def get_all_departments():
        session = create_db_connection()
        try:
            departments = session.query(Department).all()
            return departments
        finally:
            session.close()


    def get_department(department_id):
        session = create_db_connection()
        try:
            department = session.query(Department).get(department_id)
            return department
        finally:
            session.close()

    def create_department(department_data):
        session = create_db_connection()
        try:
            department = Department(**department_data)
            session.add(department)
            session.commit()
            return department
        finally:
            session.close()

    def update_department(department_id, department_data):
        session = create_db_connection()
        try:
            department = session.query(Department).get(department_id)
            if not department:
                return None
            for key, value in department_data.items():
                if hasattr(department, key):
                    setattr(department, key, value)
            session.commit()
            return department
        finally:
            session.close()

    def delete_department(department_id):
        session = create_db_connection()
        try:
            department = session.query(Department).get(department_id)
            if not department:
                return None
            session.delete(department)
            session.commit()
            return department
        finally:
            session.close()
