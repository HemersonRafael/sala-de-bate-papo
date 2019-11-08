# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Servidor de sockets TCP modificado para receber texto minusculo do cliente enviar resposta em maiuscula
#

# importacao das bibliotecas
from socket import * # sockets
import threading # threads
import time # tempo (opcional)
import json

LIST_SOCKET = {}
LIST_THREAD = []

def formatMsg(sizeMsg,nickname,command, msg):
    return json.dumps({"sizeMsg":sizeMsg,"nickname":nickname, "command": command, "msg":msg}).encode('utf-8')

def unformatMsg(data):
    return json.loads(data.decode('utf-8'))

def getCommand(command):
    a = command.split('(')
    return(a[0])

def sendAll(msg):
    for val in LIST_SOCKET:
        LIST_SOCKET[val][0].send(formatMsg(len(msg),val,'public()',msg))

def closeAll():
    for val in LIST_SOCKET:
        LIST_SOCKET[val][0].send(formatMsg(0,val,'exit()',''))
        LIST_SOCKET[val][0].close()

def listAllUser():
    users = {}
    for val in LIST_SOCKET:
        aux = '< ' + val + LIST_SOCKET[val][1] + LIST_SOCKET[val][2] + ' >\n'
        users.update({val: aux})
    return users

def saveConnection(connectionSocket, addr):
    cont = 0
    connectionSocket.send(formatMsg(0,' ','nickname()',' '))
    data = unformatMsg(connectionSocket.recv(1024)) # recebe dados do cliente
    if(data['command'] == 'nickname()'):
        for key in LIST_SOCKET:
            if(data['nickname'] == key):
                cont = cont + 1
        if(cont == 0):
            LIST_SOCKET.update({data['nickname']:[connectionSocket, addr[0], addr[1], data['nickname']]})
            print(str(LIST_SOCKET[data['nickname']][3]) + " entrou")
        else:
            aux = 'Esse nome de usuário já existir\n'
            connectionSocket.send(formatMsg(len(aux),' ','nicknameError()',aux))
    else:
        connectionSocket.send(formatMsg(0,' ','exit()',' '))
        connectionSocket.close()    

def receiveData(connectionSocket):
    sentence = connectionSocket.recv(1024) # recebe dados do cliente
    return unformatMsg(sentence)

def sendData():
    pass

# define uma classe para a criacao de threads
class minhaThread (threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self, threadConnectionSocket, threadAddr):
        threading.Thread.__init__(self)
        self.connectionSocket = threadConnectionSocket
        self.addr = threadAddr
       
    # a funcao run() e executada por padrao por cada thread 
    def run(self):
        saveConnection(self.connectionSocket,self.addr)
        print(receiveData(self.connectionSocket))
       


# definicao das variaveis
serverName = '' # ip do servidor (em branco)
serverPort = 6500 # porta a se conectar
serverSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
serverSocket.bind((serverName,serverPort)) # bind do ip do servidor com a porta
serverSocket.listen(1) # socket pronto para 'ouvir' conexoes
print ('Servidor TCP esperando conexoes na porta %d ...' % (serverPort))
cont = 0
while 1:
    connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos CLIENTES
    # criando threads
    LIST_THREAD.append(minhaThread(connectionSocket, addr))
    # disparando as threads
    LIST_THREAD[cont].start()
    cont = cont + 1
  
serverSocket.close() # encerra o socket do servidor
