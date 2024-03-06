import sqlalchemy as db
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customer"

    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    contact = db.Column(db.String, nullable=True)

    projects = relationship("Project", back_populates="customer", cascade="all, delete, delete-orphan")

class Project(Base):
    __tablename__ = "project"

    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)

    customer = relationship("Customer", back_populates="projects")
    furniture = relationship("Furniture", back_populates="project", cascade="all, delete, delete-orphan")

class Furniture(Base):
    __tablename__ = "furniture"

    furniture_id = db.Column(db.Integer, primary_key=True)
    furniture_name = db.Column(db.String)
    description = db.Column(db.String)
    serial_number = db.Column(db.String)
    amount = db.Column(db.Numeric)
    price = db.Column(db.Numeric)
    url = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey("project.project_id"))

    project = relationship("Project", back_populates="furniture")
    
