# Magic Hue lightbulb CLI utility

This repository includes two scripts:

The `setup.py` script allows the user to connect the "MagicHue" lightbulb to their Wi-Fi.
The `magichue.py` script provides an easy API for the "MagicHue" lightbulbs.

## Installation

1. Plug in your MagicHue lightbulb and turn it on. It will start flashing different colors.
2. Connect to its wifi (something like LEDnetE1234B)
3. Run the `setup.py` script, providing your SSID and your WiFi password:
`python3 setup.py -ssid MyWifiEndpoint -pswd MyAwesomePassword`

If the script worked, your lightbulb will turn green within a few seconds.

*Note: Currently the script is automated for WPA2PSK / AES only. Modify it if your WiFi uses a different mode and encryption.*

## Usage
Once your lightbulb is on your network, you can use the `magichue.py` script with the following arguments:
```
  -h, --help  show help message and exit
  -ip         provide the IP for the lightbulb; i.e. -ip 192.168.2.2
  -raw        accept colon separated raw hex string; i.e. -raw 71:23:0f
  -rgb        accept comma separated rgb values; i.e. -rgb 100,155,75
```
The user must provide the lightbulb's IP address and either comma separated RGB values or a colon separated list of HEX values. An updated list of known combinations and rules of HEX values can be found below.

#### RGB Example:
This will set the lightbulb to be red:
`python3 magichue.py -ip 192.168.2.2 -rgb 200,0,0`

#### RAW Hex Example:
This will turn the lightbulb on with its last setting:
`python3 magichue.py -ip 192.168.2.2 -raw 71:23:0f`

## Understanding the bulb's HEX codes:
I've been able to sniff a few codes, which the app sends to the lightbulb. The structure of the hex list seems to follow a pattern. The first bit defines the type of action. Then follow informational bits, which define colors, brightness, etc. The entire list is followed by a checksum bit, masked by 255. For example, this is the broken down list for turning the bulb on:

|Action bit|Body bit list|Finish bit|Checksum bit|
|---|---|---|---|
|`71`|`24`|`0f`|`a4`|

And here is how the data looks for magenta / purple color:

|Action bit|Body bit list|Finish bit|Checksum bit|
|---|---|---|---|
|`31`|`ff:2f:ff:00:f0`|`0f`|`5d`|

**It's important to note that this script will calculate the checksum bit. You MUST NOT include it in the -raw argument.**

There are several different types of commands (Action Bits) that the bulb seems to accept:
`31` - Color options
`61` - Pulse / gradual options
`71` - Power options
`81` - Status options

The `31` and `61` action bit commands seem to follow a structure in the body bit list: 
`31:RR:GG:BB:?BRIGHTNESS?:?COLORTYPE?:0f`
`61:COLOR(S):BRIGHTNESS:0f`

The following examples can help you futher undertand the structure of the body bit list:

**HEX examples**
*Note that the final checksum bit is not included here. The script will add it automatically.*
|Action Type|Values|
|---|---|
|On|`71:23:0f`|
|Off|`71:24:0f`|
|||
|RGB (255,47,255)|`31:ff:2f:ff:00:f0:0f`|
|RGB (255,126,0)|`31:ff:7e:00:00:f0:0f`|
|RGB (0,79,255)|`31:00:4f:ff:00:f0:0f`|
|||
|Warm White 100%|`31:00:00:00:ff:0f:0f`|
|Warm White 50%|`31:00:00:00:80:0f:0f`|
|Warm White 1%|`31:00:00:00:02:0f:0f`|
|||
|7 Color range, 100% speed|`61:25:1f:0f`|
|7 Color range, 50% speed|`61:25:10:0f`|
|7 Color range, 1% speed|`61:25:01:0f`|
|Red gradual, 100% speed|`61:26:1f:0f`|
|Red gradual, 50% speed|`61:26:10:0f`|
|Green gradual, 100% speed|`61:27:1f:0f`|
|Blue Gradual, 100% speed|`61:28:01:0f`|
