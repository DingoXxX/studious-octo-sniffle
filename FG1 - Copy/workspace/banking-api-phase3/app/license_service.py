from app.models import License
from app.database import SessionLocal
import datetime

def create_license(user_id: str, license_key: str):
    session = SessionLocal()
    license_obj = License(user_id=user_id, license_key=license_key,
                          expiry=datetime.datetime.utcnow() + datetime.timedelta(days=365))
    session.add(license_obj)
    session.commit()
    return {"status": "created", "license_key": license_key}

def check_license(license_key: str):
    session = SessionLocal()
    lic = session.query(License).filter(License.license_key == license_key).first()
    if lic and lic.expiry > datetime.datetime.utcnow():
        return {"status": "valid"}
    return {"status": "invalid or expired"}
