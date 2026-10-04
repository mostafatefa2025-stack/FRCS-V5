from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(200), nullable=False)
    legal_name = Column(String(200))
    cr_number = Column(String(100))
    tax_id = Column(String(100))
    sector = Column(String(100), nullable=False)
    subsector = Column(String(100))
    company_size = Column(String(50))
    ownership_type = Column(String(50))
    country = Column(String(100), default="Egypt")
    city = Column(String(100))
    currency = Column(String(10), default="EGP")
    accounting_standard = Column(String(50), default="EAS")
    fiscal_year_end = Column(String(20), default="December 31")
    established_year = Column(Integer)
    num_employees = Column(Integer)
    main_activity = Column(Text)
    contact_person = Column(String(100))
    contact_position = Column(String(100))
    phone = Column(String(50))
    email = Column(String(100))
    website = Column(String(100))
    address = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    financial_statements = relationship("FinancialStatement", back_populates="company", cascade="all, delete-orphan")

class FinancialStatement(Base):
    __tablename__ = 'financial_statements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    fiscal_year = Column(String(10), nullable=False)

    # Raw Balance Sheet
    cash_and_equiv = Column(Float, default=0.0)
    st_investments = Column(Float, default=0.0)
    accounts_receivable = Column(Float, default=0.0)
    inventory = Column(Float, default=0.0)
    other_current_assets = Column(Float, default=0.0)
    total_current_assets = Column(Float, default=0.0)
    ppe_net = Column(Float, default=0.0)
    intangible_assets = Column(Float, default=0.0)
    other_non_current_assets = Column(Float, default=0.0)
    total_assets = Column(Float, default=0.0)

    accounts_payable = Column(Float, default=0.0)
    short_term_debt = Column(Float, default=0.0)
    other_current_liabilities = Column(Float, default=0.0)
    total_current_liabilities = Column(Float, default=0.0)
    long_term_debt = Column(Float, default=0.0)
    other_non_current_liabilities = Column(Float, default=0.0)
    total_liabilities = Column(Float, default=0.0)

    common_stock = Column(Float, default=0.0)
    retained_earnings = Column(Float, default=0.0)
    total_equity = Column(Float, default=0.0)

    # Raw Income Statement
    revenue = Column(Float, default=0.0)
    cogs = Column(Float, default=0.0)
    gross_profit = Column(Float, default=0.0)
    sga_expenses = Column(Float, default=0.0)
    ebitda = Column(Float, default=0.0)
    depreciation_amort = Column(Float, default=0.0)
    ebit = Column(Float, default=0.0)
    interest_expense = Column(Float, default=0.0)
    ebt = Column(Float, default=0.0)
    tax_expense = Column(Float, default=0.0)
    net_income = Column(Float, default=0.0)

    # Raw Cash Flow Statement
    cfo = Column(Float, default=0.0)
    cfi = Column(Float, default=0.0)
    cff = Column(Float, default=0.0)
    capex = Column(Float, default=0.0)
    beginning_cash = Column(Float, default=0.0)
    ending_cash = Column(Float, default=0.0)

    company = relationship("Company", back_populates="financial_statements")
