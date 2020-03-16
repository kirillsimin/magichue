#!/usr/bin/python3

import sys
import socket
from argparse import ArgumentParser
import time

def send(text):
    ip = "10.10.123.3"
    port = 48899

    byte_array = convert_to_bytes(text)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((ip, port))
    s.send(byte_array)
    s.close()

def convert_to_bytes(message):
    encoded = ":".join("{:02x}".format(ord(c)) for c in message)
    encoded = encoded.split(':')

    values = ['0x' + s for s in encoded]
    values = [int(v,16) for v in values]
    values.append(13)
    
    return bytearray(values)

def Main(args):
    parser = ArgumentParser()
    parser.add_argument("-ssid", help="your Wi-Fi SSID; i.e. -ssid MyWifi", required=True)
    parser.add_argument("-pswd", help="your Wi-Fi Password; i.e. -pass MyPassword", required=True)
    args = parser.parse_args()
    
    send("AT+WSSSID="+args.ssid)
    print("WiFi Set")
    time.sleep(0.5)
    
    send("AT+WSKEY=WPA2PSK,AES,"+args.pswd)
    print("Password Set")
    time.sleep(0.5)

    send("AT+WMODE=STA")
    print("Switching to station mode")
    time.sleep(0.5)

    send("AT+Z")
    print("Disconnected")

if __name__ == '__main__':
    Main(sys.argv)
