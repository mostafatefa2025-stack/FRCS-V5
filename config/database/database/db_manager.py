from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DB_PATH
from database.models import Base, Company, FinancialStatement

class DatabaseManager:
    def __init__(self, db_path=None):
        path = db_path or DB_PATH
        self.engine = create_engine(f"sqlite:///{path}", echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def save_company(self, company_data):
        session = self.get_session()
        try:
            cid = company_data.get('id')
            if cid:
                comp = session.query(Company).filter_by(id=cid).first()
                for key, val in company_data.items():
                    setattr(comp, key, val)
            else:
                comp = Company(**company_data)
                session.add(comp)
            session.commit()
            session.refresh(comp)
            return comp.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_company(self, company_id):
        session = self.get_session()
        try:
            return session.query(Company).filter_by(id=company_id).first()
        finally:
            session.close()

    def list_companies(self):
        session = self.get_session()
        try:
            comps = session.query(Company).all()
            return [{"id": c.id, "name": c.company_name, "sector": c.sector, "cr": c.cr_number} for c in comps]
        finally:
            session.close()

    def save_financial_statements(self, company_id, statements_list):
        session = self.get_session()
        try:
            session.query(FinancialStatement).filter_by(company_id=company_id).delete()
            for stmt in statements_list:
                stmt['company_id'] = company_id
                fs = FinancialStatement(**stmt)
                session.add(fs)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_financial_statements(self, company_id):
        session = self.get_session()
        try:
            stmts = session.query(FinancialStatement).filter_by(company_id=company_id).order_by(FinancialStatement.fiscal_year.asc()).all()
            return [s.__dict__ for s in stmts]
        finally:
            session.close()
