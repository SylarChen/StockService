import datetime
import tushare as ts
import db_config as dbconf
import threadpool

def updateStockBasic():
    "This update all stock basic info in table STOCK_HIST_TBALE."
    #get stock basic infos from tushare API
    stock_basic = ts.get_stock_basics();
    ####################################################################################
    
    #copy index column (stock code) to a normal column, and sorted by stock code
    stock_basic.insert(0, 'stockCode', stock_basic.index)
    stock_basic = stock_basic.sort_values(by='stockCode');
    ####################################################################################
    
    #convert timeToMarket column type from int YYYYMMDD to Date
    dateToMarketList = [];
    for day in stock_basic['timeToMarket']:
        try:
            dateToMarket = datetime.datetime.strptime(str(day),'%Y%m%d');
        except Exception:
            dateToMarketList.append(None);
            continue;
        dateToMarketList.append(dateToMarket);
    stock_basic['timeToMarket'] = dateToMarketList;
    ####################################################################################
    
    #save dataframe to DB without index column
    stock_basic.to_sql(dbconf.STOCK_BASIC_TBALE_NAME, dbconf.ENGINE, if_exists='replace', index=False);
    ####################################################################################
    return

def updateStockHist(stockCode, lastRecordDate):
    "This update specific stock trade history in table STOCK_HIST_TBALE."
    print('start extract   [' + stockCode + '], lastRecordDate [' + lastRecordDate + ']');
    startTime = datetime.datetime.now();
    stock_hist = ts.get_h_data(stockCode, start=lastRecordDate)
    #when start date greater than current date, stock_hist will be NoneType
    if stock_hist is None:
        print(' ---> [' + stockCode + '] process time [' + str((datetime.datetime.now() - startTime).seconds) + 's]');
        return
    stock_hist.insert(0, 'stockCode', stockCode)
    stock_hist.insert(1, 'date', stock_hist.index)
    stock_hist.to_sql(dbconf.STOCK_HIST_TBALE_NAME, dbconf.ENGINE, index=False, if_exists='append');
    print(' ---> [' + stockCode + '] process time [' + str((datetime.datetime.now() - startTime).seconds) + 's]');
    return
    
def updateAllStockHist():
    #Get stock code list
    engine = dbconf.ENGINE;
    connection = engine.connect();
    result = connection.execute('select "stockCode" from ' + dbconf.STOCK_BASIC_TBALE_NAME);
    stockCodeList = []
    for code in result:
        stockCodeList.append(code.values()[0]);
    connection.close()
    print(stockCodeList);
    
    #Get stock last record date 
    connection = engine.connect();
    #hist table may not exist, do initial load
    try:
        result = connection.execute('select "stockCode", max("date") from ' + dbconf.STOCK_HIST_TBALE_NAME + ' group by "stockCode"');
    except Exception:
        print('No record found, going to do initial load.')
    code_date_map = {}
    for cursor in result:
        newDay = cursor.values()[1] + datetime.timedelta(1)
        code_date_map[cursor.values()[0]] = newDay.strftime("%Y-%m-%d")
    connection.close()
    print(code_date_map);
    
    #update stock hist one by one
    for stockCode in stockCodeList:
        lastRecordDate = code_date_map.get(stockCode);
        if(code_date_map.get(stockCode)==None):
            lastRecordDate = '1990-01-01';
        updateStockHist(stockCode, lastRecordDate);
    return

def updateAllStockHistMutiThread():
    #Get stock code list
    engine = dbconf.ENGINE;
    connection = engine.connect();
    result = connection.execute('select "stockCode" from ' + dbconf.STOCK_BASIC_TBALE_NAME);
    stockCodeList = []
    for code in result:
        stockCodeList.append(code.values()[0]);
    connection.close()
    print(stockCodeList);
    
    #Get stock last record date 
    connection = engine.connect();
    #hist table may not exist, do initial load
    try:
        result = connection.execute('select "stockCode", max("date") from ' + dbconf.STOCK_HIST_TBALE_NAME + ' group by "stockCode"');
    except Exception:
        print('No record found, going to do initial load.')
    code_date_map = {}
    for cursor in result:
        newDay = cursor.values()[1] + datetime.timedelta(1)
        code_date_map[cursor.values()[0]] = newDay.strftime("%Y-%m-%d")
    connection.close()
    
    #update stock hist one by one
    varsList = []
    for stockCode in stockCodeList:
        lastRecordDate = code_date_map.get(stockCode);
        if(code_date_map.get(stockCode)==None):
            lastRecordDate = '1990-01-01';
        agrsForOneStock = [stockCode, lastRecordDate]
        varsList.append((agrsForOneStock, None))
    print(varsList)
    pool = threadpool.ThreadPool(20)
    requests = threadpool.makeRequests(updateStockHist, varsList)
    [pool.putRequest(req) for req in requests]
    pool.wait()   
    return
    
#updateAllStockHistMutiThread()
# updateStockHist('000001', '1990-01-01')
# updateStockHist('000001', '2016-08-02')  
# updateStockHist('000001', '2016-08-04')

    
    
    
    
    
    
    
    
    
    
    
    
    