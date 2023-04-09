#!/bin/python3

import subprocess

print("Inserta un dominio:") 
domain = input() #Solicitamos al usuario que inserte un dominio.

data = subprocess.run('ping -c 1 -4 '+domain, shell=True, text=True, capture_output=True) #Ejecutamos el ping

if data.returncode == 0: #Realizamos comprobación de errores, si no ha salido bien el ping por lo que sea, se envía al "else".
    
    out = data.stdout #Recogemos la salida de "data"
    parserIP = out.split(" ") #Partimos la información según los espacios en una especie de "lista"
    ip = parserIP[2].replace("(","").replace(")","") #Eliminamos los paréntesis para tema visualización
    nombre_equipo = parserIP[9] #Guardamos el hostname
    ttl = int(parserIP[12].replace("ttl=","")) #Recogemos el TTL y lo transformamos a "integrer" para poder luego user operadores de comparación

    if ttl < 90:
        system = "Linux" #Si el TTL es cercano a 64 (que sea menor de 90), asumimos que es un sistema operativo Linux
    elif ttl > 90 and ttl < 200:
        system = "Windows" #Si el TTL está cercano a 128 (en concreto más de 90 y menor de 200), consideramos que es Windows
    elif ttl > 200 and ttl < 255:
        system = "Router Cisco" #Si el TTL es cercano a 254 (en concreto entre 200 y 255), consideramos que es un equipo Cisco
    else:
        system = "Sistema Operativo no encontrado." #Control de errores, por si en algún caso no saliera el TTL
        
    ttl = str(ttl) #Volvemos a transformar en "string" para concatenar más facilmente en los "print"
    print("Nombre del host: "+nombre_equipo)
    print("IP: "+ip)
    print("Sistema Operativo: "+system)
else:
    print("El dominio insertado no es correcto o no está activo.") #Control de errores, por si no saliera bien el ping inicial.