from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.collaboration import Base as CollaborationBase

Base = CollaborationBase


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    email = Column(String(50))
    phone_number = Column(String(10))
    creation_date = Column(Date)
    last_contact_date = Column(Date)
    commercial_id = Column(Integer, ForeignKey('collaborators.id'))
    company_name = Column(String(100), nullable=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)

    contact_commercial = relationship("Collaborator")
    company = relationship("Company")


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    total_amount = Column(Float)
    remaining_amount = Column(Float)
    creation_date = Column(Date)
    status = Column(Boolean, default=False)

    client = relationship("Client", backref="contracts")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    date_start = Column(Date)
    date_end = Column(Date)
    support_id = Column(Integer, ForeignKey('collaborators.id'), nullable=True)
    location = Column(String(150))
    attendees = Column(Integer)
    notes = Column(String(250))

    contract = relationship("Contract", backref="events")
    support = relationship("Collaborator", backref="events")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    phone_number = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)
    industry = Column(String(100), nullable=True)
