#!/usr/bin/python3

import sys
import socket

def Main(host,r,g,b):

    port = 5577

    s = socket.socket()
    s.connect((host, port))

    r = int(r)
    g = int(g)
    b = int(b)

    checksum = hex(0x31+r+g+b+0x00+0xf0+0x0f & 0xff)

    message = [int("0x31", 16), r, g, b, int("0x00", 16), int('0xf0',16), int('0x0f',16), int(checksum,16)]

    s.send(bytearray(message))
    s.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print ("Usage:")
        print ("\t"+sys.argv[0]+" <ip-address> <RRR> <GGG> <BBB> (colors in range 0 to 255)\n")
        print ("Example:\n\t"+sys.argv[0]+" 192.168.1.2 255 100 100")
    else:
        Main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
