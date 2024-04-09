import uuid
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as db
from sqlalchemy.schema import UniqueConstraint
from app.database import Base


class Relationship(Base):
    __tablename__ = 'relationships'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_user = db.Column(UUID, db.ForeignKey('users.id'))
    to_user = db.Column(UUID, db.ForeignKey('users.id'))

    __table_args__ = (
        UniqueConstraint('from_user', 'to_user', name='unique_relationship'),
    )
