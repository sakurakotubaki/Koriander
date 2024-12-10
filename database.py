from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./koriander.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class KorianderModel(Base):
    __tablename__ = "koriander"

    id = Column(Integer, primary_key=True, index=True)
    food = Column(String, unique=True, index=True)
    genre = Column(String)

# データベースのテーブルを作成
Base.metadata.create_all(bind=engine)
