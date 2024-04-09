import uuid
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as db
from app.database import Base

metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String, unique=True)
    hashed_password = db.Column(db.String)
