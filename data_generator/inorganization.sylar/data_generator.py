import datetime
import tushare as ts
import db_config as dbconf
import threadpool

STOCK_MARKET_START = '1990-01-01';
ENGINE = dbconf.ENGINE;

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
    stock_basic.to_sql(dbconf.STOCK_BASIC_TBALE_NAME, ENGINE, if_exists='replace', index=False);
    ####################################################################################
    return

def updateStockHist(stockCode, lastRecordDate):
    "This update specific stock trade history in table STOCK_HIST_TBALE."
    print('start extract   [' + stockCode + '], lastRecordDate [' + lastRecordDate + ']');
    startTime = datetime.datetime.now();
    stock_hist = ts.get_h_data(stockCode, start=lastRecordDate)
    #when start date greater than current date, stock_hist will be NoneType
    print(' ---> [' + stockCode + '] process time [' + str((datetime.datetime.now() - startTime).seconds) + 's]');
    if stock_hist is None:
        return
    stock_hist.insert(0, 'stockCode', stockCode)
    stock_hist.insert(1, 'date', stock_hist.index)
    stock_hist.to_sql(dbconf.STOCK_HIST_TBALE_NAME, ENGINE, index=False, if_exists='append');
    return

def removeStockHist(stockCode):
    "This remove specific stock trade history in table STOCK_HIST_TBALE."
    print('going to remove stock hist [' + stockCode + ']');
    connection = ENGINE.connect();
    result = connection.execute('delete from ' + dbconf.STOCK_HIST_TBALE_NAME + ' where "stockCode" = \'' + stockCode + '\'');
    print('[',stockCode,']',result.rowcount,'records deleted!');
    connection.close()
    
def regenerateStockHist(stockCode):
    "This remove specific stock trade history and then update it (for ex-dividend using)"
    print('going to regenerate stock hist [' + stockCode + ']');
    removeStockHist(stockCode)
    updateStockHist(stockCode, STOCK_MARKET_START)

def updateAllStockHist():
    #Get stock code list
    connection = ENGINE.connect();
    result = connection.execute('select "stockCode" from ' + dbconf.STOCK_BASIC_TBALE_NAME);
    stockCodeList = []
    for code in result:
        stockCodeList.append(code.values()[0]);
    connection.close()
    print(stockCodeList);
    
    #Get stock last record date 
    connection = ENGINE.connect();
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


updateAllStockHist()
# removeStockHist('600276');
# regenerateStockHist('600279')
# regenerateStockHist('600297')
# updateStockHist('600297', '1990-01-01')
# updateStockHist('000001', '2016-08-02')  
# updateStockHist('000001', '2016-08-04')

    
    
    
    
    
    
    
    
    
    
    
    
    