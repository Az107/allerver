#!/usr/bin/python3
import sys
import json
import curses
import socket
import argparse
import threading
from time import sleep
from math import trunc


try:
    from kernel_file import *
except ImportError:
    print("Error no se a encontrado el modulo del kernel")
    print("Imposible continuar inicio")
    exit(3)
except Exception as E:
    print(E.message)
    print("Se a encontrado un error en el kernel")
    print("imposible continuar inicio")
plugmode = True





#argumentos
parser = argparse.ArgumentParser()
parser.add_argument("-i","--interactive",help="sesion interactiva del servidor", action="store_true")

args = parser.parse_args()
fileconfig = {"IP":None,"PORT":None,"TITLE":None}
try:

    fileconfig = json.loads(open("config.json","r").read().replace("\t","").replace("\n",""))
except:
    print("No se a encontrado configuracion\n usando valores predeterminados");

comandos = dict(clear="self.clean()")
#config
IP = fileconfig["IP"] or ""
PORT = fileconfig["PORT"] or 3031
TITLE = fileconfig["TITLE"] or "servidor echo"
for plugin in fileconfig["plugins"]:
    try:
        exec("from " + plugin + " import *")
        comandos = load(comandos)
        del load
    except:
        plugmode = False
        print("plugins no disponibles")
#variables
SCREEN = curses.initscr()
SCREEN.border(0)
height, width = SCREEN.getmaxyx()
COLUMNAS = [2,trunc(width/2),width-30]
clients = []
hilos = []

    

def client_clean():
    for i in range(1,height-1):
        SCREEN.addstr(i,COLUMNAS[2],"                               ")
    SCREEN.refresh()


class consola:
    pos = 5
    prompt = ">"
    def clean(self):
        for i in range(5,height-1):
            SCREEN.addstr(i,COLUMNAS[0]+4,"                            ")
            self.pos = 5
        SCREEN.refresh()
    def puts(self,texto):
        SCREEN.addstr(self.pos,COLUMNAS[0]+4,texto)
        self.pos+=1
        SCREEN.refresh()
    def engine(self):
        curses.echo()
        curses.curs_set(1)
        while True:
            if (self.pos >= height-2):
                self.clean()

            SCREEN.addstr(self.pos,COLUMNAS[0]+4,self.prompt)
            cmd = SCREEN.getstr(self.pos,COLUMNAS[0]+4+len(self.prompt),15)
            self.pos+=1
            cmd = cmd.decode("utf-8")
            try:
                cmd = cmd.split(" ")
            except:
                cmd = (cmd,"")
              
            if (len(cmd) == 1): cmd.append("")

            if cmd[0] == "exit":
                curses.endwin()
                curses.echo()
                break
            elif cmd[0] == "test":
                self.puts("test")
            else:
                if (cmd[0] in comandos):
                    comando = comandos[cmd[0]]
                    if "$arg" in comando:
                        comando = comando.replace("$arg",cmd[1])
                    exec(comando)
                else:
                    self.puts("Comando ilegal")
            SCREEN.refresh()
        sys.exit(0)



def engine(sock,addres):
    number = clients.index((sock,addres))
    #-------------------------------------
    kernel(sock);
    #--------------------------------------
    number = clients.index((sock,addres))
    SCREEN.addstr(number+1,COLUMNAS[2],address[0]+" desconectado")
    SCREEN.refresh()
    del clients[clients.index((sock,addres))]
    sleep(2)
    client_clean()
    for client in clients:
        SCREEN.addstr(clients.index(client)+1,COLUMNAS[2],client[1][0]+" conectado      ")
    SCREEN.refresh()
    
    
    

curses.curs_set(0)
SCREEN.addstr(0,trunc(COLUMNAS[1]-len(TITLE)/2),TITLE)
SCREEN.addstr(2,COLUMNAS[0],"SERVIDOR INICIADO en " + IP + ":" + str(PORT))
SCREEN.refresh()

try:
    service = socket.socket()
    service.bind((IP,PORT))
except OSError:
    service.close()
    service.shutdown(socket.SHUT_RDWR)
    curses.endwin()
    curses.echo()
    print("El puerto esta ocupado")
    exit(2)
service.listen(5)
if (args.interactive):
    print(" interactivo")
    threading.Thread(target=consola().engine).start()
print()
try:
    while True:
        (clientsocket, address) = service.accept()
        clients.append((clientsocket,address))
        client_clean()
        for client in clients:
            SCREEN.addstr(clients.index(client)+1,COLUMNAS[2],client[1][0]+" conectado      ")
            SCREEN.refresh()
        ct = threading.Thread(target=engine,args=(clientsocket,address,))
        ct.start()
        hilos.append(ct)
except KeyboardInterrupt:
    for client in clients:
        client[0].send(tobytes("El servidor se a cerrado"))
        client[0].shutdown(socket.SHUT_RDWR)
    for hilo in hilos:
        hilo.join()
    service.shutdown(socket.SHUT_RDWR)
    service.close()
    curses.echo()
    curses.endwin()
    del SCREEN
    exit(0)
except Exception as E:
    for client in clients:
        client[0].send(tobytes("Se a producido un error y el servidor se cerrara"))
    service.shutdown(socket.SHUT_RDWR)
    curses.echo()
    curses.endwin()
    del SCREEN
    if (hasattr(E,"message")):
        print(E.message)
    else:
        print(E)
    exit(1)


