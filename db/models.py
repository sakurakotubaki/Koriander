from sqlalchemy.sql.sqltypes import String
from  db.database import Base
from sqlalchemy import Column

class DbKoriander(Base):
    __tablename__ = 'koriander'
    id = Column(Integer, primary_key=True, index=True)
    foodname = Column(String)
    genre = Column(String)