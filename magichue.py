#!/usr/bin/python3

import sys
import socket
from argparse import ArgumentParser

def add_checksum(values):
    checksum = int(hex(sum(values) & 0xff), 16)
    values.append(checksum)
    return values

def send(ip, values):
    port = 5577

    s = socket.socket()
    s.connect((ip, port))
    
    s.send(bytearray(add_checksum(values)))
    s.close()

def process_raw(raw):
    raw = raw.split(':')
    values = ['0x' + s for s in raw]
    values = [int(v,16) for v in values]
    return values

def process_rgb(rgb):
    rgb = rgb.split(',')
    if len(rgb) < 3: print_error('Must have three color values (0-255) for R,G,B')

    values = [int(v) for v in rgb]
    values.insert(0,49) # add header
    values.extend([0,240,15]) # add tail
    return values

def print_error(message):
    print('\n' + esc('31;1') + ' ERROR' + esc(0) + ' : ' + message)
    print(' Run with -h for help.\n')
    sys.exit()

def esc(code):
    return f'\033[{code}m'

def Main(args):
    parser = ArgumentParser()
    parser.add_argument("-ip", help="provide the IP for the lightbulb; i.e. -ip 192.168.2.2")
    parser.add_argument("-raw", help="accept colon separated raw hex string; i.e. -raw 71:23:0f")
    parser.add_argument("-rgb", help="accept comma separated rgb values; i.e. -rgb 100,155,75")
    args = parser.parse_args()

    if args.ip is None:
        print_error('Must provide IP.')

    if args.raw is not None:
        values = process_raw(args.raw)

    if args.rgb is not None:
        values = process_rgb(args.rgb)

    if 'values' in locals():
        send(args.ip, values)
    else:
        print_error('Must provide raw hex or rgb values.')

if __name__ == '__main__':
    Main(sys.argv)
