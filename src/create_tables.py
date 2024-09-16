# create_tables.py

from database import engine, SessionLocal
from models import Base, City, Product, Month, Stock

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 定义城市、月份和产品列表
cities = ['上海', '广州', '武汉', '北京', '济南', '苏州', '常熟', '泰安', '深圳', '珠海']
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
products = ['品牌茶饮', '品牌果汁', '品牌咖啡', '品牌汽水', '品牌饮用水',
            '网红茶饮', '网红果汁', '网红咖啡', '网红汽水', '网红饮用水',
            '自营茶饮', '自营咖啡', '自营果汁', '自营汽水', '自营饮用水']

def populate_tables():
    db = SessionLocal()
    try:
        # 填充 Months 表
        for month_id in months:
            month = Month(month_id=month_id, month=month_id)
            db.merge(month)

        # 填充 Cities 表
        for city_id, city_name in enumerate(cities, start=1):
            city = City(city_id=city_id, city_name=city_name)
            db.merge(city)

        # 填充 Products 表
        for product_id, product_name in enumerate(products, start=1):
            product = Product(product_id=product_id, product_name=product_name)
            db.merge(product)

        db.commit()

        # 填充 Stock 表
        stock_entries = []

        # 查询插入的城市、月份和产品
        cities_db = db.query(City).all()
        months_db = db.query(Month).all()
        products_db = db.query(Product).all()

        for month in months_db:
            for city in cities_db:
                for product in products_db:
                    stock_entry = Stock(
                        month_id=month.month_id,
                        city_id=city.city_id,
                        product_id=product.product_id,
                        quantity=0
                    )
                    stock_entries.append(stock_entry)

        db.bulk_save_objects(stock_entries)
        db.commit()

        print(f"Stock 表已填充，共 {len(stock_entries)} 条记录。")

    finally:
        db.close()

if __name__ == "__main__":
    populate_tables()
