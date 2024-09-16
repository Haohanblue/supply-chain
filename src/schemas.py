# schemas.py
from pydantic import BaseModel
from typing import List

class City(BaseModel):
    city_id: int
    city_name: str

    class Config:
        from_attributes = True

class Month(BaseModel):
    month_id: int
    month: int

    class Config:
        from_attributes = True

class Product(BaseModel):
    product_id: int
    product_name: str

    class Config:
        from_attributes = True

class Stock(BaseModel):
    stock_id: int
    month_id: int
    city_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class StockUpdate(BaseModel):
    quantity: int

class StockBulkModifyItem(BaseModel):
    city_id: int
    product_id: int
    month: int
    quantity: int
    operation: str  # 操作类型：'update'、'increase'、'decrease'

class StockBulkModify(BaseModel):
    updates: List[StockBulkModifyItem]
