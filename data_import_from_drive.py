
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import pymysql
from sqlalchemy import create_engine



srcPath = './NSE_Data/data/temp/onemin_dump/2020/IntradayData_JAN2020/'
srcPath = './NSE_Data/data/temp/onemin_dump/IntradayData_JAN_JUN2019/IntradayData_JAN_JUN2019/'

# flist= [f.path.replace('\\','/') for f in os.scandir(srcPath) if f.is_dir()]
temp = [f for f in listdir(srcPath) if isfile(join(srcPath, f))]

flist = []

# filters = ["_F1","_F2"]
filters = []
for f in temp:
    if not any(x in f for x in filters):
        tmpStr = srcPath + '/' + f
        flist.append(tmpStr.replace('//','/'))


print(flist)
data = pd.DataFrame()

for f in flist:
    # print(f + '/' + filename)    
    print('Opening...' + f)
    temp = pd.read_csv(f,names=['ticker', 'date','time','open','high','low','close','volume','garbage'], low_memory = False)
    temp = temp.drop(['garbage'],axis=1)
    data = data.append(temp,ignore_index=True)

data['temp'] = data['date'].astype(str) +' '+ data['time']
data['datetime'] = pd.to_datetime(data['temp'],format = '%Y%m%d %H:%M')
data = data.drop(['date','time','temp'],axis=1)
data.set_index('datetime',inplace=True)

print(data.dtypes)
print(data)
# print(data.to_sql())




# Connect to the database
sqlEngine = create_engine('mysql+pymysql://root:@127.0.0.1/test', pool_recycle=3600)
dbConnection = sqlEngine.connect()


# connection = pymysql.connect(host='localhost',
# user='root',
# password='',
# db='test',
# charset='utf8mb4',
# cursorclass=pymysql.cursors.DictCursor)

# try:
#   with connection.cursor() as cursor:
#     # Create a new record
#     sql = "INSERT INTO `nse_nifty50_data` (`email`, `password`) VALUES (%s, %s)"
#     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
 
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#   connection.commit()
 
#   with connection.cursor() as cursor:
#     # Read a single record
#     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
#     cursor.execute(sql, ('webmaster@python.org',))
#     result = cursor.fetchone()
#     print(result)
# finally:
#   connection.close()

data.to_sql('nse_nifty50_data', con = dbConnection, if_exists = 'append', chunksize = 1000)
dbConnection.close()