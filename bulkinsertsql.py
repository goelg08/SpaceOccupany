import pandas as pd
#import sqlalchemy
import pypyodbc

#from sqlalchemy import create_engine
 
data=[('10.128.40.8','Python Programming','Active'),('10.128.40.32','Learn MySQL','Active'),('10.128.40.33','Data Science Cookbook','Active')]

data.append[VALUES]
#engine = create_engine('mssql+pyodbc://@localhost/demo?driver=SQL+Server+Native+Client+11.0')

#data.to_sql('pinginfo', con = engine, if_exists = 'append', chunksize = 1000)


conn = pypyodbc.connect('Driver={SQL Server};'
										'Server=localhost;'
										'Database=Demo;'
										'Trusted_Connection=yes')
cursor = conn.cursor()
SQLCommand = ("INSERT INTO Demo.dbo.pinginfo(IPAddr, HostName, Status) VALUES(?,?,?)")
#Values = [ip,host_name,status]
cursor.executemany(SQLCommand,data)	
conn.commit()
print ("Data inserted")
conn.close()