# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Servidor de sockets TCP modificado para receber texto minusculo do cliente enviar resposta em maiuscula
#

# importacao das bibliotecas
from socket import *  # sockets
import threading  # threads
import time  # tempo (opcional)
import json

LIST_SOCKET = {}
LIST_THREAD = []
chat = []


def formatMsg(sizeMsg, nickname, command, msg):
    return json.dumps(
        {"sizeMsg": sizeMsg, "nickname": nickname, "command": command, "msg": msg}
    ).encode("utf-8")


def unformatMsg(data):
    return json.loads(data.decode("utf-8"))


def getCommand(command):
    a = command.split("(")
    return a[0]


def getNickname(data):
    data = data.split("(")
    data = data[1].split(")")
    return data[0]


def sendAll(msg):
    for val in LIST_SOCKET:
        x = LIST_SOCKET[val][0]
        x.send(formatMsg(len(msg), val, "public()", msg))


def closeAll():
    for val in LIST_SOCKET:
        LIST_SOCKET[val][0].send(formatMsg(0, val, "exit()", ""))
        LIST_SOCKET[val][0].close()


def listAllUser():
    users = {}
    for val in LIST_SOCKET:
        aux = "< " + val + LIST_SOCKET[val][1] + LIST_SOCKET[val][2] + " >\n"
        users.update({val: aux})
    return users


def receiveData(connectionSocket):  
    data = connectionSocket.recv(1024)
    msgReceive = unformatMsg(data)  # recebe do servidor a resposta)
    if msgReceive["command"] == "nickname()":
        nameExist = False
        for key in LIST_SOCKET:
            if msgReceive["nickname"] == key:
                nameExist = True
                break

        if nameExist == False:
            LIST_SOCKET.update(
                {
                    msgReceive["nickname"]: [
                        connectionSocket,
                        addr[0],
                        addr[1],
                        msgReceive["nickname"],
                    ]
                }
            )
            x = str(LIST_SOCKET[msgReceive["nickname"]][3] + " entrou")
            chat.append(x)
            a = SendThread(connectionSocket, formatMsg(0, " ", "nickname()", " "))
            a.start()
            sendAll(x)
        else:
            aux = "Esse nome de usuário já existir\n"
            connectionSocket.send(formatMsg(len(aux), " ", "nicknameError()", aux))

    elif msgReceive.get("command") == "public()":
        aux = msgReceive.get("nickname") + " escreveu: " + msgReceive.get("msg")
        chat.append(aux)
    elif getCommand(msgReceive.get("command")) == "private":
        for key in LIST_SOCKET:
            if msgReceive[getNickname(msgReceive.get("command"))] == key:
                m = SendThread(
                    LIST_SOCKET[key],
                    formatMsg(
                        len(msgReceive.get("msg")),
                        msgReceive.get("nickname"),
                        msgReceive.get("command"),
                        msgReceive.get("msg"),
                    ),
                )
    elif msgReceive.get("command") == "list()":
        print('list')
        for key in LIST_SOCKET:
            if msgReceive["nickname"] == key:
                m = SendThread(
                    LIST_SOCKET[key],
                    formatMsg(
                        len(listAllUser()),
                        msgReceive.get("nickname"),
                        msgReceive.get("command"),
                        listAllUser(),
                    ),
                )
    elif msgReceive.get("command") == "exit()":
        aux = msgReceive.get("nickname") + " saiu " 
        chat.append(aux)
        sendAll(aux)


# define uma classe para a criacao de threads
class minhaThread(threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self, threadConnectionSocket, threadAddr):
        threading.Thread.__init__(self)
        self.connectionSocket = threadConnectionSocket
        self.addr = threadAddr

    # a funcao run() e executada por padrao por cada thread
    def run(self):
        a = SendThread(connectionSocket, formatMsg(0, " ", "nickname()", " "))
        a.start()
        receiveData(self.connectionSocket)


class SendThread(threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self, socketThread, msgThread):
        threading.Thread.__init__(self)
        self.msg = msgThread
        self.socket = socketThread

    # a funcao run() e executada por padrao por cada thread
    def run(self):
        self.socket.send(self.msg)


# definicao das variaveis
serverName = ""  # ip do servidor (em branco)
serverPort = 6500  # porta a se conectar
serverSocket = socket(AF_INET, SOCK_STREAM)  # criacao do socket TCP
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((serverName, serverPort))  # bind do ip do servidor com a porta
serverSocket.listen(1)  # socket pronto para 'ouvir' conexoes
print("Servidor TCP esperando conexoes na porta %d ..." % (serverPort))
contThread = 0
while 1:
    connectionSocket, addr = serverSocket.accept()  # aceita as conexoes dos CLIENTES
    # criando threads
    LIST_THREAD.append(minhaThread(connectionSocket, addr))
    # disparando as threads
    LIST_THREAD[contThread].start()
    contThread = contThread + 1
    
    for x in range(len(chat)):
        print(chat[x])

serverSocket.close()  # encerra o socket do servidor

