# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Cliente de sockets TCP modificado para enviar texto minusculo ao servidor e aguardar resposta em maiuscula
#

# importacao das bibliotecas
from socket import *
import threading  # threads
import json
import time  # tempo (opcional)
import os

# definicao das variaveis
serverName = "127.0.0.1"  # ip do servidor
serverPort = 6500  # porta a se conectar
clientSocket = socket(AF_INET, SOCK_STREAM)  # criacao do socket TCP
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
clientSocket.connect((serverName, serverPort))  # conecta o socket ao servidor
chat = []
msgSend = []
userOn = []


def formatMsg(sizeMsg, nickname, command, msg):
    return json.dumps(
        {"sizeMsg": sizeMsg, "nickname": nickname, "command": command, "msg": msg}
    ).encode("utf-8")


def unformatMsg(data):
    data = data.decode("utf-8")
    x = json.loads(data)
    return x


def getCommand(command):
    a = command.split("(")
    return a[0]

def getNickname(data):
    data = data.split("(")
    data = data[1].split(")")
    return data[0]


class SendThread(threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self, msgThread):
        threading.Thread.__init__(self)
        self.msg = msgThread

    # a funcao run() e executada por padrao por cada thread
    def run(self):
        clientSocket.send(self.msg)


class RecvThread(threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self):
        threading.Thread.__init__(self)

    # a funcao run() e executada por padrao por cada thread
    def run(self):
        data = clientSocket.recv(1024)
        msgReceive = unformatMsg(data)  # recebe do servidor a resposta)
        if msgReceive.get("command") == "public()":
            aux = msgReceive.get("nickname") + " escreveu: " + msgReceive.get("msg")
            chat.append(aux)
        elif getCommand(msgReceive.get("command")) == "private":
            aux = (
                msgReceive.get("nickname")
                + " escreveu privado para vôce: "
                + msgReceive.get("msg")
            )
            chat.append(aux)
        elif msgReceive.get("command") == "list()":
            chat.append(" Lista de usuário online: ", msgReceive.get("msg"))
        elif msgReceive.get("command") == "exit()":
            aux = msgReceive.get("nickname") + " saiu."
            chat.append(aux)
        elif msgReceive["command"] == "nicknameError()":
            print("O nickname informado já existir!")
            nickName = input("Para conctar-se a sala de bate papo informe seu nickname: ")
            a = SendThread(formatMsg(0, nickName, "nickname()", ""))
            a.start()
            os.system("reset")
        else:
            pass


while True:

    data = unformatMsg(clientSocket.recv(1024))

    if data["command"] == "nickname()":
        nickName = input("Para conctar-se a sala de bate papo informe seu nickname: ")
        a = SendThread(formatMsg(0, nickName, "nickname()", ""))
        a.start()
        break
    else:
        os.system("reset")

r = RecvThread()
r.start()

while True:
    if len(chat) > 0:
        for x in range(len(chat)):
            print(chat[x])

    sentence = input("Digite a mensagem ou comando: ")
    if getCommand(sentence) == "private":
        msg = input("Informe a mensagem privada: ")
        b = SendThread(formatMsg(len(sentence), nickName, sentence, msg))
        b.start()
    elif sentence == "list()":
        c = SendThread(formatMsg(0, nickName, sentence, ""))
        c.start()
    elif sentence == "exit()":
        d = SendThread(formatMsg(0, nickName, sentence, ""))
        d.start()
        break
    else:
        e = SendThread(formatMsg(len(sentence), nickName, "public()", sentence))
        e.start()

    #os.system("reset")
clientSocket.close()  # encerramento o socket do cliente
