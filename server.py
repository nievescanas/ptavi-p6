#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import sys
import socketserver
import os.path as path

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    """
    Comprueba si existe el fichero y lo utiliza como diccionario
    """
    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
            # Leyendo línea a línea lo que nos envía el cliente
        for line in self.rfile:
            if not line or line.decode('utf-8') == "\r\n":
                continue
            else:
                print(line.decode('utf-8'))
                line = (line.decode('utf-8').split())

                if line[0] == 'INVITE':
                    line = 'SIP/2.0 ' + '100 ' + 'Trying\r\n\r\n'
                    line += 'SIP/2.0 ' + '180 ' + 'Ringing\r\n\r\n'
                    line += 'SIP/2.0 ' + '200 ' + 'OK\r\n\r\n'
                    self.wfile.write(bytes(line, 'utf-8'))
                elif line[0] == 'BYE':
                    line = 'SIP/2.0 ' + '200 ' + 'OK\r\n\r\n'
                    self.wfile.write(bytes(line, 'utf-8'))
                elif line[0] != ('INVITE' and 'BYE'):
                    line = 'SIP/2.0 ' + '405 ' + 'Method Not Allowed\r\n\r\n'
                    self.wfile.write(bytes(line, 'utf-8'))
                elif line[2] != ('SIP/2.0') :
                    line = 'SIP/2.0 ' + '400 ' + ' Bad Request\r\n\r\n'
                    self.wfile.write(bytes(line, 'utf-8'))                    
                    

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos

    try:
        sys.argv[2] == int
        len(sys.argv) != 4
        if path.exists(sys.argv[3]):
            print('Listening...')
        else:
            raise IndexError      
    except IndexError:
        sys.exit("Usage: python3 server.py IP port audio_file")

    serv = socketserver.UDPServer(('', int(sys.argv[2])), EchoHandler)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")        


    
    
    
