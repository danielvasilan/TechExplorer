#~/prod_service/app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from pydantic.schema import date

app = FastAPI()

fake_prod_db = [
    {
        'wo_code': 'W001',
        'prod_date': '2020-06-01',
        'prod_qty': 7,
        'wc_list': ['CR', 'CUS', 'TLP']
    }


]


class ProdDec(BaseModel):
    wo_code: str
    prod_date: date
    prod_qty: int
    wc_list: List[str]


@app.get('/', response_model=List[ProdDec])
async def index():
    return fake_prod_db

@app.post('/', status_code=201)
async def add_prod_dec(payload: ProdDec):
    new_pd = payload.dict()
    fake_prod_db.append(new_pd)
    return {'id': len(fake_prod_db) -1}
