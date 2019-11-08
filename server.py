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

def formatMsg(sizeMsg,nickname,command, msg):
    return json.dumps({"sizeMsg":sizeMsg,"nickname":nickname, "command": command, "msg":msg}).encode('utf-8')

def unformatMsg(data):
    return json.loads(data.decode('utf-8'))

def getCommand(command):
    a = command.split('(')
    return(a[0])

def saveConnection(connectionSocket):
    connectionSocket.send(formatMsg(0,' ','nickname()',' '))
    data = unformatMsg(connectionSocket.recv(1024)) # recebe dados do cliente
    if(data['command'] == 'nickname()'):
        LIST_SOCKET.update({addr[0]:[connectionSocket, addr[0], addr[1], data['nickname']]})
    else:
        connectionSocket.send(formatMsg(0,' ','exit()',' '))
        connectionSocket.close()    

def to_receive(connectionSocket):
    connectionSocket.send(formatMsg(0,' ','nickname()',' '))
    sentence = connectionSocket.recv(1024) # recebe dados do cliente
    print(unformatMsg(sentence))
    connectionSocket.send(formatMsg(2,'server','public()','oi'))
    #connectionSocket.close() # encerra o socket com o cliente

# define uma classe para a criacao de threads
class minhaThread (threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self, threadConnectionSocket):
        threading.Thread.__init__(self)
        self.connectionSocket = threadConnectionSocket
       
    # a funcao run() e executada por padrao por cada thread 
    def run(self):
        saveConnection(self.connectionSocket)
        to_receive(self.connectionSocket)
       

# definicao das variaveis
serverName = '192.168.1.100' # ip do servidor (em branco)
serverPort = 6500 # porta a se conectar
serverSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
serverSocket.bind((serverName,serverPort)) # bind do ip do servidor com a porta
serverSocket.listen(1) # socket pronto para 'ouvir' conexoes
print ('Servidor TCP esperando conexoes na porta %d ...' % (serverPort))

while 1:
    connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos CLIENTES
    
    #salve_cliente(connectionSocket, addr)
    # criando threads
    thread1 = minhaThread(connectionSocket)
    # disparando as threads
    thread1.start()
  
serverSocket.close() # encerra o socket do servidor
