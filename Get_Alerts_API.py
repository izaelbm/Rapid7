#!/usr/bin/python

#importando bibliotecas
import http.client
import json 
from datetime import datetime, timedelta,date
import mysql.connector

#conectando ao DB Mysql
try:
    con_db = mysql.connector.connect(user='root', password='root', host='127.0.0.1',database='rapid7')
    print("Conetado")
except:
    print("Erro ao Conectar")

cursor = con_db.cursor()

#conetando a API
def getAPI(index,start,end,size):
    conn = http.client.HTTPSConnection("us.api.insight.rapid7.com")
    payload = ''
    headers = {
    'Accept-version': 'investigations-preview',
    'x-api-key': 'YXF1aSBuYW8gdGljbyB0aWNv'
    }
    conn.request("GET", "/idr/v2/investigations?start_time="+str(start)+"T00:00:00Z&size="+str(size)+"&end_time="+str(end)+"T23:59:59Z&index="+str(index), payload, headers)
    res = conn.getresponse()
    data = res.read()

    return json.loads(data)

start = date.today() - timedelta(days=1)
end = date.today() - timedelta(days=1)

#start = "2022-01-01"
#end = "2022-01-31"

meta = getAPI(1,start,end,1) 

pages = round(meta['metadata']['total_pages']/100)

#ajustando numero de paginas caso for 0
if pages < 1:
    pageLimit = 1
else:
    pageLimit = pages

for i in range(pageLimit):
    index = i
    log = getAPI(index,start,end,100) 
    
    for dt in log['data']:
    
        insert_stmt = (
            "INSERT INTO LOGS(rrn, organization_id, title, source,status,priority, last_accessed, created_time, disposition, assignee_name, assignee_email, first_alert_time, latest_alert_time, date)"
            "VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s)"
        )
        
        if dt['assignee'] == None:
            assignee_name = " "
            assignee_email = " "
        else:
            assignee_name = dt['assignee']['name']
            assignee_email = dt['assignee']['email']


        data = (dt['rrn'],dt['organization_id'],dt['title'],dt['source'],dt['status'],dt['priority'],dt['last_accessed'],dt['created_time'],dt['disposition'],assignee_name,assignee_email,dt['first_alert_time'],dt['latest_alert_time'],date.today())
        
        try:
            # Executing the SQL command
            cursor.execute(insert_stmt, data)
            # Commit your changes in the database
            con_db.commit()
        except:
            # Rolling back in case of error
            con_db.rollback()
            print("Data inserted")
            # Closing the connection
            con_db.close()
print("Concluido")
