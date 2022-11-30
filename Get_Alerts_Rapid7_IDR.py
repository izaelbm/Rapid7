#!/usr/bin/python
# encoding: utf-8

#importando bibliotecas
import http.client
import json
from datetime import datetime, timedelta,date
import os
import time

#funcao para inserir os dados no arquivo
def insertData(date,string):
    nw_date = str(date).replace("-","_")
    name_file = "ReportR7.txt"
#name_file = "ReportR7_"+str(nw_date)+".txt"
    report = open(name_file, 'a')
    report.write(string.strip()+"\n")

#API Alertas
def getAlertsAPI(index,start,end,size):
    conn = http.client.HTTPSConnection("us.api.insight.rapid7.com")
    payload = ''
    headers = {
    'Accept-version': 'investigations-preview',
    'x-api-key': '0123456789'
    }
    conn.request("GET", "/idr/v2/investigations?start_time="+str(start)+"T00:00:00Z&size="+str(size)+"&end_time="+str(end)+"T23:59:59Z&index="+str(index), payload, headers)
    res = conn.getresponse()
    data = res.read()

    return json.loads(data)

#API Alerta
def getAlertAPI(id):
    conn = http.client.HTTPSConnection("us.api.insight.rapid7.com")
    payload = ''
    headers = {
    'Accept-version': 'investigations-preview',
    'x-api-key': '0123456789'
    }
    conn.request("GET", "/idr/v2/investigations/"+str(id), payload, headers)
    res = conn.getresponse()
    data = res.read()

    return json.loads(data)

#API Comentarios
def getCommentsAPI(id):
    conn1 = http.client.HTTPSConnection("us.api.insight.rapid7.com")
    payload1 = ''
    headers1 = {
    'Accept-version': 'comments-preview',
    'x-api-key': '0123456789'
    }
    conn1.request("GET", "/idr/v1/comments?target="+id+"&size=100&index=0", payload1, headers1)
    res1 = conn1.getresponse()
    data1 = res1.read()
    
    try:
        return json.loads(data1)
    except:
        return "null"

#setando o intervalo do relatorio
#start = "2022-11-03"
#start = date.today() - timedelta(days=1)
#end = date.today() - timedelta(days=1)
#end = "2022-11-03"

#inserindo o cabecalho no arquivo
insertData(date.today(),"ID;ORGANIZATION_ID;TITLE;SOURCE;STATUS;PRIORITY;LAST_ACCESSED;CREATED_TIME;DISPOSITION;ASSIGNEE;FIRST_ALERT_TIME;LATEST_ALERT_TIME;COMMENTS;TYPE;CATEGORIE;SUBCATEGORIE;TEAM;RISK;AREA;SOURCE;ACTOR;MANAGER")


for i in range(60):

    start = date.today() - timedelta(days=i)
    end = date.today() - timedelta(days=i)

    
    #contando a quantidade de paginas
    count = getAlertsAPI(0,start,end,1)

    pages_alerts = round(count['metadata']['total_pages']/100)

    #Ajustando numero de paginas caso for 0
    if pages_alerts < 1:
        pageLimit = 1
    else:
        pageLimit = pages_alerts

    #iniciando as variaveis
    id = ""
    organization_id = ""
    title = ""
    source = ""
    status = ""
    priority = ""
    last_accessed = ""
    created_time = ""
    disposition = ""
    first_alert_time = ""
    latest_alert_time = ""

    #lendo os alertas
    for i in range(pageLimit):
        index = i
        Alerts = getAlertsAPI(index,start,end,100)
        
        #capturando o ID do Alerta
        for data in Alerts['data']:
            
            #capturando o id do alerta
            id = data['rrn']
            
            #Pesquisando o alerta por ID
            Alert = getAlertAPI(id)
            
            #consultando os comentarios
            Comments = getCommentsAPI(id) 
            
            coment_data = "#"
            Alert_type = "#"
            Alert_categorie = "#"
            Alert_subcategorie = "#"
            Alert_team = "#"
            Alert_risk = "#"
            Alert_area = "#"
            Alert_source = "#"
            Alert_actor = "#"
            Alert_manager = "#"
            
            #verificando se o alerta possui comentarios
            if Comments == "null":
                coment_data = "#"
                Alert_type = "#"
                Alert_categorie = "#"
                Alert_subcategorie = "#"
                Alert_team = "#"
                Alert_risk = "#"
                Alert_area = "#"
                Alert_source = "#"
                Alert_actor = "#"
                Alert_manager = "#"
            else:
                coment_data = ""
                for data_coment in Comments['data']:
                    
                    if data_coment['body'] is None:
                        print("Comentario Vazio")
                    else:
                        tags = data_coment['body'].split('#')                   

                        if(data_coment['body'][0] == "#"):
                            #removendo os #
                            data_coment['body'] = data_coment['body'].replace("#","")
                            
                            #quebrando a string em array
                            array_comments = data_coment['body'].split("\n")
                            
                            Alert_type = str(array_comments[0].strip())
                            Alert_categorie = str(array_comments[1].strip())
                            Alert_subcategorie = str(array_comments[2].strip())
                            Alert_team = str(array_comments[3].strip())
                            Alert_risk = str(array_comments[4].strip())
                            Alert_area = str(array_comments[5].strip())
                            Alert_source = str(array_comments[6].strip())
                            Alert_actor = str(array_comments[7].strip())
                            Alert_manager = str(array_comments[8].strip())
                        else:
                            print("bypass")

                    
            try:   
                #validando se o alerta foi assinado
                if Alert['assignee'] is None:
                    assignee_name = "#"
                    assignee_email = "#"
                else:
                    assignee_name = Alert['assignee']['name']
                    assignee_email = Alert['assignee']['email']
            except:
                assignee_name = "#"
                assignee_email = "#"
                
            #Validando os Dados

            #Id Alerta
            if Alert['rrn'] is None:
                id = "#"
            else:
                id = Alert['rrn']

            #Id Organizacao
            if Alert['organization_id'] is None:
                organization_id = "#"
            else:
                organization_id = Alert['organization_id']

            #Titulo
            if Alert['title'] is None:
                title = "#"
            else:
                title = Alert['title']
            
            #Origem
            if Alert['source'] is None:
                source = "#"
            else:
                source = Alert['source']

            #Status
            if Alert['status'] is None:
                status = "#"
            else:
                status = Alert['status']

            #Prioridade
            if Alert['priority'] is None:
                priority = "#"
            else:
                priority = Alert['priority']

            #Ultimo Acesso
            if Alert['last_accessed'] is None:
                last_accessed = "#"
            else:
                last_accessed = Alert['last_accessed']

            #Data Cricao
            if Alert['created_time'] is None:
                created_time = "#"
            else:
                created_time = Alert['created_time']

            #Disposicao
            if Alert['disposition'] is None:
                disposition = "#"
            else:
                disposition = Alert['disposition']

            #Data Abertura
            if Alert['first_alert_time'] is None:
                first_alert_time = str(date.today())
            else:
                first_alert_time = Alert['first_alert_time']

            #Data Encerramento
            if Alert['latest_alert_time'] is None:
                latest_alert_time = first_alert_time
            else:
                latest_alert_time = Alert['latest_alert_time']

            #Comentarios
            if coment_data is None:
                coment_data = "#"
            

            #inserindo os registros no arquivo
            try:
                time.sleep(10)            
                insertData(date.today(),str(id+";" + organization_id +";"+ title +";"+ source +";"+ status +";"+ priority +";"+ last_accessed +";"+ created_time +";"+ disposition +";"+ assignee_name +";"+ first_alert_time +";"+ latest_alert_time +";"+coment_data+";"+Alert_type+";"+Alert_categorie+";"+Alert_subcategorie+";"+Alert_team+";"+Alert_risk+";"+Alert_area+";"+Alert_source+";"+Alert_actor+";"+Alert_manager+";"))
                
            except Exception as e:
                print("Erro" + str(e) + str(id))
            
    print("Concluido...")
