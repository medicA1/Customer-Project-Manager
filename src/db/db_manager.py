from db.db_model import Customer, Project, Furniture
from sqlalchemy import func, or_
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

class SessionManager():
    def __init__(self, path):
        self.path = path

    def create_session(self):
        engine = db.create_engine(f"sqlite:///{self.path}")
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        return session

class DatabaseManager():
    def __init__(self, session):
        self.session = session
    
    def get_customers(self):
        return self.session.query(Customer).all()

    def get_customer_name_surname(self, customer_id):
        customer = self.session.query(Customer).filter(Customer.id == customer_id).first()
        if customer:
            return customer.name, customer.surname
        else:
            return None, None

    def get_customer_by_id(self, customer_id):
        customer = self.session.query(Customer).filter(Customer.id == customer_id).first()
        return customer

    def add_new_customer(self, name, surname):
        customer = Customer(name=name, surname=surname)
        self.session.add(customer)
        self.session.commit()
        return customer

    def rename_customer(self, new_name, new_surname, customer):
        if customer:
            customer.name = new_name
            customer.surname = new_surname
            return customer
        
    def delete_customer_by_id(self, customer_id):
        try:
            customer = self.session.query(Customer).filter(Customer.id == customer_id).one()
            self.session.delete(customer)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False
        
    def search_like_customer(self, search_term):
        search_term = search_term.lower()
        results = self.session.query(Customer).filter(
            or_(
                func.lower(Customer.name + ' ' + Customer.surname).ilike(f'%{search_term}%'),
                func.lower(Customer.surname + ' ' + Customer.name).ilike(f'%{search_term}%')
            )
        ).all()
        return results

    def get_projects(self, customer_id):
        projects = self.session.query(Project).filter(Project.customer_id == customer_id).all()
        if projects:
            return [project.project_name for project in projects]
        else:
            return []
    
    def add_project(self, project_name, customer_id):
        project = Project(project_name=project_name, customer_id=customer_id)
        self.session.add(project)
        self.session.commit()

    def get_project_id(self, project_name):
        project = self.session.query(Project).filter(Project.project_name == project_name).first()
        if project:
            return project.project_id
        return False
    
    def get_project_name_by_id(self, project_id):
        project = self.session.query(Project).filter(Project.project_id == project_id).first()
        if project:
            return project.project_name
    
    def delete_project_by_project_id(self, project_id):
        try:
            project = self.session.query(Project).filter(Project.project_id == project_id).one()
            self.session.delete(project)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def add_furniture_data(self, name, description, serial_number, amount, price, url, project_id):
        furniture = Furniture(furniture_name=name, description=description, serial_number=serial_number, amount=amount, price=price, url=url, project_id=project_id)
        self.session.add(furniture)
        self.session.commit()

    def delete_furniture_by_furniture_id(self, furniture_id):
        try:
            furniture = self.session.query(Furniture).filter(Furniture.furniture_id==furniture_id).one()
            self.session.delete(furniture)
            self.session.commit()
            return True
        except:
            self.session.rollback()
            return False

    def get_total_price_by_project_id(self, project_id):
        total_price = self.session.query(func.sum(Furniture.price * Furniture.amount)).filter(Furniture.project_id == project_id).scalar()
        return total_price

    def fetch_furniture_data(self, project_id):
        results = self.session.query(
            Furniture.furniture_id,
            Furniture.furniture_name,
            Furniture.description,
            Furniture.serial_number,
            Furniture.amount,
            Furniture.price,
            Furniture.url
            ).filter(Furniture.project_id == project_id).all()
        
        furniture_list = [
        {
            "furniture_id": result[0],  
            "furniture_name": result[1],
            "description": result[2],
            "serial_number": result[3],
            "amount": result[4],
            "price": result[5],
            "url": result[6]
        }
        for result in results
        ]
        
        return furniture_list
    

