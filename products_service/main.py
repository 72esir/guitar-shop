from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, database

# Создаем таблицы в БД (если их нет)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product