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
clientes = {'0.0.0.0':'teste'}
ips = ['0.0.0.0']
def salve_cliente(connectionSocket, addr):
    
    if(ips.count(addr[0]) == 0):
        ips.append(addr[0])
        connectionSocket.send("informe o seu nickname".encode('utf-8'))
        sentence = connectionSocket.recv(1024) # recebe dados do cliente
        name = sentence.decode('utf-8')   
        clientes.update({addr[0]:name})
    else:
        pass


def to_receive(connectionSocket):
    sentence = connectionSocket.recv(1024) # recebe dados do cliente
    sentence = sentence.decode('utf-8')
    capitalizedSentence = sentence.upper() # converte em letras maiusculas
    print ('Cliente %s enviou: %s, transformando em: %s' % (addr, sentence, capitalizedSentence))
    print(clientes)
    connectionSocket.send(capitalizedSentence.encode('utf-8')) # envia para o cliente o texto transformado
    connectionSocket.close() # encerra o socket com o cliente

# define uma classe para a criacao de threads
class minhaThread (threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self, threadConnectionSocket):
        threading.Thread.__init__(self)
        self.connectionSocket = threadConnectionSocket
       
    # a funcao run() e executada por padrao por cada thread 
    def run(self):
        to_receive(self.connectionSocket)
       

# definicao das variaveis
serverName = '127.0.0.1' # ip do servidor (em branco)
serverPort = 6500 # porta a se conectar
serverSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
serverSocket.bind((serverName,serverPort)) # bind do ip do servidor com a porta
serverSocket.listen(1) # socket pronto para 'ouvir' conexoes
print ('Servidor TCP esperando conexoes na porta %d ...' % (serverPort))
while 1:
  connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos clientes
  salve_cliente(connectionSocket, addr)
  # criando threads
  thread1 = minhaThread(connectionSocket)
  # disparando as threads
  thread1.start()
  
serverSocket.close() # encerra o socket do servidor