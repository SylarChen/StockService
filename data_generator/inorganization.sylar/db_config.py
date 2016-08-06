from sqlalchemy import create_engine
import os

try:
    db_url = os.environ['DB_URL'];
except Exception:
    print('Cant find Environment Variable DB_URL')
    return;
print(db_url)
ENGINE = create_engine(db_url)
STOCK_HIST_TBALE_NAME = 'hist';
STOCK_BASIC_TBALE_NAME = 'basic';