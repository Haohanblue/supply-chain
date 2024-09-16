# main.py
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 导入 CORS 中间件
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
from typing import List
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import defer, joinedload
app = FastAPI()

# 配置 CORS 中间件，允许任何来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],    # 允许所有 HTTP 方法
    allow_headers=["*"],    # 允许所有请求头
)

# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# main.py
@app.get("/stocks/", response_model=List[schemas.Stock])
def get_stocks(db: Session = Depends(get_db)):
    stocks = db.query(models.Stock).all()
    return stocks

@app.put("/stocks/clear_all/")
def clear_all_stocks(db: Session = Depends(get_db)):
    try:
        # 将所有库存数量置为零
        db.query(models.Stock).update({models.Stock.quantity: 0})
        db.commit()
        return {"msg": "所有库存已清空"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="清空库存时发生错误")
    
@app.put("/stocks/bulk_modify/")
def bulk_modify_stocks(
    bulk_update: schemas.StockBulkModify,
    db: Session = Depends(get_db)
):
    # 收集所有需要更新的条件
    criteria = []
    city_ids = set()
    product_ids = set()
    min_month = 13
    for update_item in bulk_update.updates:
        operation = update_item.operation.lower()
        if operation not in ["update", "increase", "decrease"]:
            raise HTTPException(
                status_code=400,
                detail=f"无效的操作类型：{update_item.operation}，应为 'update'、'increase' 或 'decrease'"
            )
        criteria.append({
            'city_id': update_item.city_id,
            'product_id': update_item.product_id,
            'start_month': update_item.month,
            'quantity': update_item.quantity,
            'operation': operation
        })
        city_ids.add(update_item.city_id)
        product_ids.add(update_item.product_id)
        if update_item.month < min_month:
            min_month = update_item.month

    # 一次性查询所有相关的库存记录
    months = list(range(min_month, 13))
    stocks = db.query(models.Stock).filter(
        models.Stock.city_id.in_(city_ids),
        models.Stock.product_id.in_(product_ids),
        models.Stock.month_id.in_(months)
    ).all()

    # 创建库存记录的映射
    stock_map = {}
    for stock in stocks:
        key = (stock.city_id, stock.product_id, stock.month_id)
        stock_map[key] = stock

    # 批量更新库存记录
    updated_stocks = []
    for item in criteria:
        city_id = item['city_id']
        product_id = item['product_id']
        start_month = item['start_month']
        quantity = item['quantity']
        operation = item['operation']

        for month_id in range(start_month, 13):
            key = (city_id, product_id, month_id)
            stock = stock_map.get(key)
            if not stock:
                continue
            if operation == 'update':
                stock.quantity = quantity
            elif operation == 'increase':
                stock.quantity += quantity
            elif operation == 'decrease':
                if stock.quantity < quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"库存不足：city_id={city_id}, product_id={product_id}, month={month_id}"
                    )
                stock.quantity -= quantity
            updated_stocks.append(stock)

    # 一次性提交事务
    db.commit()
# Mount the dist directory at the root URL
app.mount("/", StaticFiles(directory="dist", html=True), name="dist")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8712, reload=True)
