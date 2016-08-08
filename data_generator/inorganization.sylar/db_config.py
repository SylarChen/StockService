from sqlalchemy import create_engine
import os

try:
    db_url = os.environ['DB_URL'];
except Exception:
    print('ERROR: Cant find Environment Variable DB_URL!!!')
    db_url='postgresql://postgres:sylar@127.0.0.1/postgres'
    print('Set Default URL to', db_url)
    
print(db_url)
ENGINE = create_engine(db_url)
STOCK_HIST_TBALE_NAME = 'hist';
STOCK_BASIC_TBALE_NAME = 'basic';
