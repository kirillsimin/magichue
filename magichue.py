#!/usr/bin/python3

import sys
import socket
from argparse import ArgumentParser

def add_checksum(values):
    checksum = int(hex(sum(values) & 0xff), 16)
    values.append(checksum)
    return values

def get_status(ip):
    try: 
        data = bytearray(process_raw('81:8a:8b:96'))
        
        s = socket.socket()
        s.settimeout(5)
        s.connect((ip,5577))
        s.send(data)
        response = s.recvfrom(1024)
        s.close()
        response = [hex(s).replace('0x', '') for s in response[0]]
        response = [ '0'+s if len(s) == 1 else s for s in response]
        return response
    except:
        print_error("Could not get the bulb's status")
        return None


def get_version(ip):
    try: 
        data = bytearray(process_raw('48:46:2d:41:31:31:41:53:53:49:53:54:48:52:45:41:44')) #HF-A11ASSISTHREAD
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        s.sendto(data, (ip,48899))
        response = s.recvfrom(1024)
        s.close()
        msg = response[0].decode('utf-8')
        version = msg.split(',')
        
        return version[2]
    except:
        print_error("Could not get the bulb's version")
        return None

def send(ip, values):
    try:
        get_version(ip)

        s = socket.socket()
        s.connect((ip, 5577))
        s.send(bytearray(add_checksum(values)))
        s.close()
        print({'success':'true'})
    except:
        print_error("Could not send the message to the bulb")

def process_raw(raw):
    raw = raw.split(':')
    values = ['0x' + s for s in raw]
    values = [int(v,16) for v in values]
    return values

def process_rgb(rgb, version):
    rgb = rgb.split(',')
    if len(rgb) < 3: print_error('Must have three color values (0-255) for R,G,B')

    values = [int(v) for v in rgb]
    values.insert(0,49) # add header

    # this version has an extra zero in the body
    if version == "AK001-ZJ2101":
        values.extend([0])

    values.extend([0,240,15]) # add tail
    return values

def process_power(power):
    if power == 'on':
        return process_raw('71:23:0f')
    if power == 'off':
        return process_raw('71:24:0f')

def print_error(message):
    out = {'success':'false', 'error':message}
    print(out)
    sys.exit()

def Main(args):
    parser = ArgumentParser()
    parser.add_argument("-ip", help="provide the IP for the lightbulb; i.e. -ip 192.168.2.2")
    parser.add_argument("-raw", help="accept colon separated raw hex string; i.e. -raw 71:23:0f")
    parser.add_argument("-rgb", help="accept comma separated rgb values; i.e. -rgb 100,155,75")
    parser.add_argument("-warm", help="accept value of warm white (0-255); i.e. -warm 150")
    parser.add_argument("-power", help="accept 'on' or 'off'; i.e. -power on")
    parser.add_argument("-status", help="get the bulb's status", action='store_true')
    parsed_args = parser.parse_args()


    if parsed_args.ip is None:
        print_error('Must provide IP.')

    if parsed_args.status is True:
        status = get_status(parsed_args.ip)
        
        power = status[2]
        power = 'on' if power == '23' else power
        power = 'off' if power == '24' else power
        
        rgb = status[6:9]
        for i,c in enumerate(rgb):
            rgb[i] = int('0x'+c, 16)
        
        warm = int('0x'+status[9], 16)
        
        print ({'power' : power, 'rgb' : rgb, 'warm' : warm})
        return

    if parsed_args.raw is not None:
        values = process_raw(parsed_args.raw)

    if parsed_args.rgb is not None:
        version = get_version(parsed_args.ip)
        if version is None: sys.exit()
        values = process_rgb(parsed_args.rgb, version)

    if parsed_args.warm is not None:
        warm = hex(int(parsed_args.warm)).replace('0x','')
        values = process_raw('31:00:00:00:'+warm+':0f:0f')

    if parsed_args.power is not None:
        values = process_power(parsed_args.power)

    if 'values' in locals():
        send(parsed_args.ip, values)

    else:
        print_error('Must provide raw hex or rgb values.')

if __name__ == '__main__':
    Main(sys.argv)

