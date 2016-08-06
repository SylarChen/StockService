from sqlalchemy import create_engine
import os

os.environ['DB_URL'] = 'postgresql://postgres:sylar@127.0.0.1/postgres'
try:
    db_url = os.environ['DB_URL'];
except Exception:
    print('WARN: Cant find Environment Variable DB_URL!!!')
print(db_url)
ENGINE = create_engine(db_url)
STOCK_HIST_TBALE_NAME = 'hist';
STOCK_BASIC_TBALE_NAME = 'basic';