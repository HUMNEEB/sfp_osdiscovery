# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_osdiscovery
# Purpose:      SpiderFoot plug-in for show the Hostname, IP and Operative System by writting a domain.
#
# Author:      Juan Carlos Anguix Monzó <SpieldoseMusic@gmail.com>
# Coauthor:      Daniel García Baameiro <dagaba13@gmail.com>
#
# Created:     15/05/2022
# Copyright:   (c) Juan Carlos Anguix Monzó & Daniel García Baameiro 2022
# Licence:     GPL
# -------------------------------------------------------------------------------


from spiderfoot import SpiderFootEvent, SpiderFootPlugin
import subprocess


class sfp_osdiscovery(SpiderFootPlugin):

    meta = {
        'name': "Operative System Discovery",
        'summary': "Shows the Hostname, IP and the Operative System by writting a domain.",
        'flags': [""],
        'useCases': [""],
        'categories': ["Passive DNS"]
    }

    # Default options
    opts = {
    }

    # Option descriptions
    optdescs = {
    }

    results = None

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    def watchedEvents(self):
        return ["DOMAIN_NAME"]

    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    def producedEvents(self):
        return ["PROVIDER_DNS", "IP_ADDRESS", "OPERATING_SYSTEM"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.sf.debug(f"Received event, {eventName}, from {srcModuleName}")

        try:
            self.sf.debug(f"We use the data: {eventData}")
            print(f"We use the data: {eventData}")

            ########################
            # Insert here the code #
            ########################
            data = subprocess.run('ping -c 1 -4 '+eventData, shell=True, text=True, capture_output=True) #Ejecutamos el ping
                          
            out = data.stdout #Recogemos la salida de "data"
            print(out)
            parserIP = out.split(" ") #Partimos la información según los espacios en una especie de "lista"
            print(parserIP)
            ip = parserIP[2].replace("(","").replace(")","") #Eliminamos los paréntesis para tema visualización
            print(ip)
            nombre_equipo = parserIP[9] #Guardamos el hostname
            print(nombre_equipo)
            ttl = int(parserIP[12].replace("ttl=","")) #Recogemos el TTL y eliminamos el texto "ttl="

            if ttl < 90:
                system = "Linux" #Si el TTL es cercano a 64 (que sea menor de 90), asumimos que es un sistema operativo Linux
            elif ttl > 90 and ttl < 200:
                system = "Windows" #Si el TTL está cercano a 128 (en concreto más de 90 y menor de 200), consideramos que es Windows
            elif ttl > 200 and ttl < 255:
                system = "Router Cisco" #Si el TTL es cercano a 254 (en concreto entre 200 y 255), consideramos que es un equipo Cisco
            else:
                system = "Sistema Operativo no encontrado." #Control de errores, por si en algún caso no saliera el TTL
                
            ########################
            print(ttl)
            
            if not ttl:
                self.sf.error("Unable to perform <ACTION MODULE> on " + eventData)
                return
        except Exception as e:
            self.sf.error("Unable to perform the <ACTION MODULE> on " + eventData + ": " + str(e))
            return

        evt = SpiderFootEvent("PROVIDER_DNS", nombre_equipo, self.__name__, event)
        self.notifyListeners(evt)

        evt = SpiderFootEvent("IP_ADDRESS", ip, self.__name__, event)
        self.notifyListeners(evt)
        
        evt = SpiderFootEvent("OPERATING_SYSTEM", system, self.__name__, event)
        self.notifyListeners(evt)
        
# End of sfp_osdiscovery class