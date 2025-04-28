from google.cloud.sql.connector import Connector
from flask_sqlalchemy import SQLAlchemy

connector = Connector(refresh_strategy="lazy")
db = SQLAlchemy()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "creator": lambda: connector.connect(
            "acssz-default:europe-west4:default",
            "pg8000",
            user="ezclaim-invoiceservice",
            password="ezclaim-invoiceservice",
            db="invoice",
            ip_type="public"
        )
    }
    db.init_app(app)
    return app
