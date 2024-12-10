from pydantic import BaseModel

class KorianderBase(BaseModel):
    food: str # 食べ物の名前
    genre: str # 食べ物の分類

class KorianderCreate(KorianderBase):
    pass

class Koriander(KorianderBase):
    id: int

    class Config:
        from_attributes = True