from sqlalchemy.orm import Session
from db.models import DbKoriander
from schemas import KorianderBase

# create Koriander
def create_koriander(db: Session, request: KorianderBase):
    new_koriander = DbKoriander(
        foodname=request.foodname,
        genre=request.genre,
    )
    db.add(new_koriander)
    db.commit()
    db.refresh(new_koriander)
    return new_koriander

# read all elements
def get_koriander(db: Session):
    return db.query(DbKoriander).all()

# read one elements
def get_korianders(db: Session, koriander_id: int):
    return db.query(DbKoriander).filter(DbKoriander.id == koriander_id).first()