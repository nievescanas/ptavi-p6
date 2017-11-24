#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""
import os
import sys
import socket

# Cliente UDP simple.
try:
    if 'INVITE' != sys.argv[1]:
        if 'BYE' != sys.argv[1]:
            raise IndexError
    if len(sys.argv) != 3:
        raise IndexError
except IndexError:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")

if sys.argv[1] == 'INVITE' or 'BYE':
    LINE = sys.argv[1] + ' sip:'
    LINE += sys.argv[2][:sys.argv[2].rfind(':')] + ' SIP/2.0\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    PORT = int(sys.argv[2][sys.argv[2].rfind(':')+1:])
    SERVER = str(sys.argv[2][sys.argv[2].find('@')+1:sys.argv[2].rfind(':')])
    my_socket.connect((SERVER, PORT))

    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)

    if data.decode('utf-8') != '':
        mensaje = (data.decode('utf-8').split())
        if 'Trying'in mensaje:
            if 'Ringing'in mensaje:
                if 'OK' in mensaje:
                    LINE = 'ACK' + ' sip:'
                    LINE += sys.argv[2][:sys.argv[2].rfind(':')]
                    LINE += ' SIP/2.0\r\n'
            my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')

    print(data.decode('utf-8'))
