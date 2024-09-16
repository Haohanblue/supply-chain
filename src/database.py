# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://haohanblue:Haohanblue233.@bj-cynosdbmysql-grp-3upmvv08.sql.tencentcdb.com:27017/warehouse"

engine = create_engine(
    DATABASE_URL,
    echo=True,  # 输出SQL语句，方便调试
    pool_pre_ping=True  # 检查连接是否有效
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
