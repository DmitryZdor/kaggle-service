from sqlalchemy import Column, Integer, String
from db_connect import Base


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    size = Column(Integer)
    zip_arch = Column(String)
    owner = Column(String)
