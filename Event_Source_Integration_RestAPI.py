#!/usr/bin/python3.6

#importando bibliotecas
import socket
import json
import http.client


host="127.0.0.1"
port=6675
url_provider="us.rest.logs.insight.rapid7.com"


#Testando a Conexao  ao coletor do Rapid7 - UDP
sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rs = sc.connect_ex((host,port))

if (rs == 0):
        print("Conectou")
else:
        print("Erro ao Conectar")

#conectando a RestAPI
import http.client

conn = http.client.HTTPSConnection(url_provider)
payload = ''
headers = {
  'x-api-key': '123123123123123123123123123123'
}
conn.request("GET", "/log_search/management/logs/2c8ff074-35f9-4031-9dc3-6cfe5a4d4e75", payload, headers)
res = conn.getresponse()
data = res.read()

#Tratando os logs
data = data.decode("utf-8")

byte_message=bytes (f"{data}", "utf-8")


#Enviando os logs ao Coletor do Rapid7
try:
        #sc.sendto(data.encode('utf-8'), (host, port))
        sc.sendto(byte_message,(host,port))

        print("Log Enviado")
finally:
        sc.close()
