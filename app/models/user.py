from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, JSON, DateTime
from sqlalchemy.orm import relationship
from app.schemas import user as userSchemas

from app.config.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    gender = Column(String, default=userSchemas.Gender.MALE)
    address = Column(JSON, nullable=True)
    disable_date = Column(Date, default=None)
    batch_date = Column(Date, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #items = relationship("Item", back_populates='owner')

    @property
    def _serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'gender': self.gender,
            'age': self.age,
            'address': self.address,
            'is_active': self.is_active,
            'disable_date': self.disable_date,
            'batch_date': self.batch_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }




# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(200), index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey('users.id'))

#     owner = relationship('User', back_populates='items')