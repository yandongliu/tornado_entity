from sqlalchemy import Column, Integer, String
from sqlalchemy.types import CHAR

from models.base import Base

class Entity(Base):

    __tablename__ = 'entity'

    id = Column(Integer, primary_key=True)
    uuid = Column(CHAR(36), nullable=True, index=True)

    def __init__(self):
        pass
