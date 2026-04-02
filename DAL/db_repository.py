from .db_models import (
    Application,
    Customer,
    Developer,
    FreeApplication,
    PaidApplication,
    Release,
    Review,
    Transaction,
)
from .interfaces import IDBRepository


class DBRepository(IDBRepository):
    def __init__(self, session):
        self.session = session

    def _get_or_create_developer(self, row):
        developer = self.session.query(Developer).filter_by(email=row["developer_email"]).first()
        if developer is None:
            developer = Developer(
                username=row["developer_username"],
                email=row["developer_email"],
                developer_name=row["developer_name"],
                website=row["developer_website"],
            )
            self.session.add(developer)
            self.session.flush()
        return developer

    def _get_or_create_customer(self, row):
        customer = self.session.query(Customer).filter_by(email=row["customer_email"]).first()
        if customer is None:
            customer = Customer(
                username=row["customer_username"],
                email=row["customer_email"],
                payment_method=row["customer_payment_method"],
            )
            self.session.add(customer)
            self.session.flush()
        return customer

    def _get_or_create_application(self, row, developer):
        app = (
            self.session.query(Application)
            .filter_by(title=row["application_title"], developer_id=developer.id)
            .first()
        )

        if app is not None:
            app.version = row["application_version"]
            return app

        if row["application_type"] == "paid_application":
            app = PaidApplication(
                title=row["application_title"],
                version=row["application_version"],
                price=row["paid_price"] if row["paid_price"] is not None else 0.99,
                developer=developer,
            )
        else:
            app = FreeApplication(
                title=row["application_title"],
                version=row["application_version"],
                contains_ads=bool(row["free_contains_ads"]),
                developer=developer,
            )

        self.session.add(app)
        self.session.flush()
        return app

    def _create_release_if_missing(self, row, app):
        release = (
            self.session.query(Release)
            .filter_by(application_id=app.app_id, version_tag=row["release_version_tag"])
            .first()
        )
        if release is None:
            self.session.add(
                Release(
                    version_tag=row["release_version_tag"],
                    release_notes=row["release_notes"],
                    upload_date=row["release_date"],
                    application=app,
                )
            )

    def _link_download_if_needed(self, row, customer, app):
        if row["downloaded"] and app not in customer.downloaded_applications:
            customer.downloaded_applications.append(app)

    def _create_review_if_needed(self, row, customer, app):
        if not row["has_review"]:
            return

        exists = (
            self.session.query(Review)
            .filter_by(
                application_id=app.app_id,
                customer_id=customer.id,
                date=row["review_date"],
                comment=row["review_comment"],
            )
            .first()
        )
        if exists is None:
            self.session.add(
                Review(
                    rating=row["review_rating"],
                    comment=row["review_comment"],
                    date=row["review_date"],
                    application=app,
                    customer=customer,
                )
            )

    def _create_transaction_if_needed(self, row, customer, app):
        if not row["has_transaction"] or row["transaction_id"] is None:
            return

        if not isinstance(app, PaidApplication):
            return

        exists = self.session.query(Transaction).filter_by(transaction_id=row["transaction_id"]).first()
        if exists is None:
            self.session.add(
                Transaction(
                    transaction_id=row["transaction_id"],
                    amount=row["transaction_amount"] if row["transaction_amount"] is not None else app.price,
                    date=row["transaction_date"],
                    customer=customer,
                    paid_application=app,
                )
            )

    def paste_all_data(self, rows):
        try:
            for row in rows:
                developer = self._get_or_create_developer(row)
                customer = self._get_or_create_customer(row)
                app = self._get_or_create_application(row, developer)

                self._create_release_if_missing(row, app)
                self._link_download_if_needed(row, customer, app)
                self._create_review_if_needed(row, customer, app)
                self._create_transaction_if_needed(row, customer, app)

            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
