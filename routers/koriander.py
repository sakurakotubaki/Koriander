from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from schemas import KorianderBase, KorianderCreate, Koriander
from database import SessionLocal, KorianderModel

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/koriander", response_model=Koriander, status_code=status.HTTP_201_CREATED)
async def create_koriander(koriander: KorianderCreate, db: Session = Depends(get_db)):
    # 重複チェック
    existing_koriander = db.query(KorianderModel).filter(KorianderModel.food == koriander.food).first()
    if existing_koriander:
        raise HTTPException(status_code=400, detail="Food already exists")

    db_koriander = KorianderModel(**koriander.dict())
    db.add(db_koriander)
    try:
        db.commit()
        db.refresh(db_koriander)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create koriander")
    return db_koriander

@router.get("/koriander", response_model=List[Koriander])
async def get_all_koriander(db: Session = Depends(get_db)):
    return db.query(KorianderModel).all()

@router.get("/koriander/{id}", response_model=Koriander)
async def get_koriander(id: int, db: Session = Depends(get_db)):
    db_koriander = db.query(KorianderModel).filter(KorianderModel.id == id).first()
    if db_koriander is None:
        raise HTTPException(status_code=404, detail="Koriander not found")
    return db_koriander

@router.put("/koriander/{id}", response_model=Koriander)
async def update_koriander(id: int, koriander: KorianderBase, db: Session = Depends(get_db)):
    db_koriander = db.query(KorianderModel).filter(KorianderModel.id == id).first()
    if db_koriander is None:
        raise HTTPException(status_code=404, detail="Koriander not found")
    
    # 重複チェック（food名を変更する場合）
    if koriander.food != db_koriander.food:
        existing_koriander = db.query(KorianderModel).filter(KorianderModel.food == koriander.food).first()
        if existing_koriander:
            raise HTTPException(status_code=400, detail="Food already exists")
    
    for key, value in koriander.dict().items():
        setattr(db_koriander, key, value)
    
    try:
        db.commit()
        db.refresh(db_koriander)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update failed")
    return db_koriander

@router.delete("/koriander/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_koriander(id: int, db: Session = Depends(get_db)):
    db_koriander = db.query(KorianderModel).filter(KorianderModel.id == id).first()
    if db_koriander is None:
        raise HTTPException(status_code=404, detail="Koriander not found")
    
    try:
        db.delete(db_koriander)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Delete failed")