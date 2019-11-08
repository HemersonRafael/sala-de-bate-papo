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
serverName = '127.0.0.1' # ip do servidor
serverPort = 6500 # porta a se conectar
clientSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
clientSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1) 
clientSocket.connect((serverName, serverPort)) # conecta o socket ao servidor
chat = []
userOn = []

def formatMsg(sizeMsg,nickname,command, msg):
    return json.dumps({"sizeMsg":sizeMsg,"nickname":nickname, "command": command, "msg":msg}).encode('utf-8')

def unformatMsg(data):
    return json.loads(data.decode('utf-8'))

def getCommand(command):
    a = command.split('(')
    return(a[0])

def getNickname(data):
    data = data.split('(')
    data = data[1].split(')')
    return data[0]

nickName = input('Para conctar-se a sala de bate papo informe seu nickname: ')
data = unformatMsg(clientSocket.recv(1024))

if(data['command'] == 'nickname()'):
    clientSocket.send(formatMsg(0,nickName,'nickname()',''))

while True:
    msgReceive= unformatMsg(clientSocket.recv(1024)) # recebe do servidor a resposta
    if(msgReceive.get('command') == 'public()'):
        aux = msgReceive.get('nickname') + ' escreveu: ' + msgReceive.get('msg')
        chat.append(aux)
    elif(getCommand(msgReceive.get('command')) == 'private'):
        aux = msgReceive.get('nickname') + ' escreveu privado para vôce: ' + msgReceive.get('msg')
        chat.append(aux)
    elif(msgReceive.get('command') == 'list()'):
        print(' Lista de usuário online: ', msgReceive.get('msg'))
    elif(msgReceive.get('command') == 'exit()'):
        aux = msgReceive.get('nickname') + ' saiu.'
        chat.append(aux)
    for x in range(len(chat)): 
        print(chat[x])
        
    sentence = input('Digite a mensagem ou comando: ') 
    if(getCommand(sentence) == 'private'):
        msg = input('Informe a mensagem privada: ')
        clientSocket.send(formatMsg(len(sentence), nickName, sentence, msg))
    elif(sentence == 'list()'):
        clientSocket.send(formatMsg(0, nickName, sentence, ''))
    elif (sentence == 'exit()'):
        clientSocket.send(formatMsg(0, nickName, sentence, ''))
        break
    else:
        clientSocket.send(formatMsg(len(sentence), nickName, 'public()', sentence))

clientSocket.close() # encerramento o socket do cliente
