# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Cliente de sockets TCP modificado para enviar texto minusculo ao servidor e aguardar resposta em maiuscula
#

# importacao das bibliotecas
from socket import *
import threading # threads
import json

# definicao das variaveis
serverName = '192.168.1.100' # ip do servidor
serverPort = 6500 # porta a se conectar
clientSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
clientSocket.connect((serverName, serverPort)) # conecta o socket ao servidor
conversa = []

def formatMsg(sizeMsg,nickname,command, msg):
    return json.dumps({"sizeMsg":sizeMsg,"nickname":nickname, "command": command, "msg":msg}).encode('utf-8')
def unformatMsg(data):
    return json.loads(data.decode('utf-8'))
def getCommand(command):
    a = command.split('(')
    return(a[0])


nickName = input('Para conctar-se a sala de bate papo informe seu nickname: ')
data = unformatMsg(clientSocket.recv(1024))
if(data[command] == 'nickName()'):
    clientSocket.send(formatMsg(0,nickName,'nickname()',''))

while True:
    sentence = input('Digite a mensagem: ') 
    if(sentence == 'exit()'):
    elif(sentence == '')
    conteudo = str([len(sentence),'rafael','publica',sentence])
    clientSocket.sendall(conteudo.encode('utf-8')) # envia o texto para o servidor
    modifiedSentence = clientSocket.recv(1024) # recebe do servidor a resposta
    print ('O servidor (\'%s\', %d) respondeu com: %s' % (serverName, serverPort, modifiedSentence.decode('utf-8')))
clientSocket.close() # encerramento o socket do cliente
