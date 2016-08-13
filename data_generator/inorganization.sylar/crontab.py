import data_generator as dg
import datetime

dg.updateStockBasic()
dg.updateAllStockHist()
print("Job End At : ", str(datetime.datetime.now()))