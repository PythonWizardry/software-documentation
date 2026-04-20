from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .interfaces import IDBModels


Base = declarative_base()


customer_applications = Table(
	"customer_applications",
	Base.metadata,
	Column("customer_id", Integer, ForeignKey("customers.id"), primary_key=True),
	Column("application_id", Integer, ForeignKey("applications.app_id"), primary_key=True),
)


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False)
	email = Column(String, nullable=False)
	user_type = Column(String(50), nullable=False)

	__mapper_args__ = {
		"polymorphic_on": user_type,
		"polymorphic_identity": "user",
	}


class Developer(User):
	__tablename__ = "developers"

	id = Column(Integer, ForeignKey("users.id"), primary_key=True)
	developer_name = Column(String, nullable=False)
	website = Column(String)

	applications = relationship("Application", back_populates="developer")

	__mapper_args__ = {
		"polymorphic_identity": "developer",
	}


class Customer(User):
	__tablename__ = "customers"

	id = Column(Integer, ForeignKey("users.id"), primary_key=True)
	payment_method = Column(String)

	downloaded_applications = relationship(
		"Application",
		secondary=customer_applications,
		back_populates="customers",
	)
	reviews = relationship("Review", back_populates="customer")
	transactions = relationship("Transaction", back_populates="customer")

	__mapper_args__ = {
		"polymorphic_identity": "customer",
	}


class Application(Base):
	__tablename__ = "applications"

	app_id = Column(Integer, primary_key=True)
	title = Column(String, nullable=False)
	version = Column(String, nullable=False)
	app_type = Column(String(50), nullable=False)
	developer_id = Column(Integer, ForeignKey("developers.id"), nullable=False)

	developer = relationship("Developer", back_populates="applications")
	releases = relationship("Release", back_populates="application", cascade="all, delete-orphan")
	reviews = relationship("Review", back_populates="application", cascade="all, delete-orphan")
	customers = relationship(
		"Customer",
		secondary=customer_applications,
		back_populates="downloaded_applications",
	)

	__mapper_args__ = {
		"polymorphic_on": app_type,
		"polymorphic_identity": "application",
	}


class FreeApplication(Application):
	__tablename__ = "free_applications"

	app_id = Column(Integer, ForeignKey("applications.app_id"), primary_key=True)
	contains_ads = Column(Boolean, nullable=False, default=False)

	__mapper_args__ = {
		"polymorphic_identity": "free_application",
	}


class PaidApplication(Application):
	__tablename__ = "paid_applications"

	app_id = Column(Integer, ForeignKey("applications.app_id"), primary_key=True)
	price = Column(Float, nullable=False)

	transactions = relationship("Transaction", back_populates="paid_application")

	__mapper_args__ = {
		"polymorphic_identity": "paid_application",
	}


class Release(Base):
	__tablename__ = "releases"

	id = Column(Integer, primary_key=True)
	version_tag = Column(String, nullable=False)
	release_notes = Column(String)
	upload_date = Column(Date, nullable=False)
	application_id = Column(Integer, ForeignKey("applications.app_id"), nullable=False)

	application = relationship("Application", back_populates="releases")


class Review(Base):
	__tablename__ = "reviews"

	id = Column(Integer, primary_key=True)
	rating = Column(Integer, nullable=False)
	comment = Column(String)
	date = Column(Date, nullable=False)
	application_id = Column(Integer, ForeignKey("applications.app_id"), nullable=False)
	customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

	application = relationship("Application", back_populates="reviews")
	customer = relationship("Customer", back_populates="reviews")


class Transaction(Base):
	__tablename__ = "transactions"

	transaction_id = Column(String, primary_key=True)
	amount = Column(Float, nullable=False)
	date = Column(Date, nullable=False)
	customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
	paid_application_id = Column(Integer, ForeignKey("paid_applications.app_id"), nullable=False)

	customer = relationship("Customer", back_populates="transactions")
	paid_application = relationship("PaidApplication", back_populates="transactions")

class DBModels(IDBModels):
    def __init__(self, engine):
        self.engine = engine

    def create_tables(self):
        Base.metadata.create_all(self.engine)
