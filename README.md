# Pychonet

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]


A library for interfacing with the ECHONETlite protocol as commonly used in Japan.
Useful for interfacing to many interesting devices such as HVACs,
electric car chargers, rice cookers (not joking), and solar systems
that support ECHONETLite.

The current functionality is limited to a few ECHONETLite classes, notably HVAC
but it can easily be extended to any ECHONETlite classes required.

The basic boilerplate EchoNetInstance class can be used to provide
raw connectivity to any compatible device but it is up to the developer
to create useful classes. Any ECHONETlite class additions to the library are welcome.

Version 2.0.0 of this libray was rebuilt to use asyncio for better compatability with home assistant.


It is designed to work with Python 3.9.5+

## Instructions

Simplest way to install is to use pip:

```
pip install pychonet
```

## Basic usage

## create the ECHONETLite listener service on port 3610
```python
from aioudp import UDPServer
from pychonet import Factory
from pychonet import ECHONETAPIClient as api
from pychonet import HomeAirConditioner
from pychonet import EchonetInstance
udp = UDPServer()
loop = asyncio.get_event_loop()
udp.run("0.0.0.0",3610, loop=loop)
server = api(server=udp,loop=loop)
```

### Discover a list of ECHONETlite instances on a particular server using:
```python
await server.discover('192.168.1.6')
```


### Popualte the propertymap for a particular ECHONETLite instance
```python
await server.getAllPropertyMaps('192.168.1.6',1,48,1)
```
# create a ECHONETLite device using the Factory.
# paramaters include the port listener, and EOJGC, EOJCC, and EOJCI codes
```python
aircon = Factory("192.168.1.6",server, 1,48,1)
```

# OR, create a specific ECHONETLite instance using built in objects.
```python
aircon = HomeAirConditioner("192.168.1.6", server )
```

### Turn HVAC on or off:
```python
await aircon.on()
await aircon.off()
await aircon.getOperationalStatus()
{'status': 'off'}
```

### Set or Get a HVACs target temperature
```python
await aircon.setOperationalTemperature(25)
await aircon.getOperationalTemperature()
{'set_temperature': 25}
```

### Set or Get a HVACs mode of operation:
```python
supported modes =  'auto', 'cool', 'heat', 'dry', 'fan_only', 'other'

await aircon.setMode('cool')
await aircon.getMode()
{'mode': 'cool'}
```
### Set or Get a HVACs fan speed:

Note - your HVAC may not support all fan speeds.
```python
supported modes = 'auto', 'minimum', 'low', 'medium-Low', 'medium', 'medium-high', 'high', 'very high', 'max'

await aircon.setFanSpeed('medium-high')
await aircon.getFanSpeed()
{'fan_speed': 'medium-high'}
```
### Get HVAC attributes at once (Note, the property map must be populated):
```python
await aircon.update()
{'status': 'On', 'set_temperature': 25, 'fan_speed': 'medium-high', 'room_temperature': 25, 'mode': 'cooling'}
```

### OR grab a specific attribute at once (Note, the property map must be populated):
```python
await aircon.update(0x80)
```

## Using this library with Home Assistant

NOTE: For Home Assistant users there is now a dedicated repo for the related Home Assistant 'Mitsubishi' custom component that makes use of this Python library:
(https://github.com/scottyphillips/mitsubishi_hass)

'example_hvac.py' gives you an idea how to drive a HVAC directly from Python using this library.

## Hall of Fame
Thanks to khcnz (Karl Chaffey) and gvs for helping refector the old code
and contributing to testing.

Thanks to Dick Swart, Masaki Tagawa, Paul, khcnz,  Kolodnerd, and Alfie Gerner
for each contributing code updates to to the original 'mitsubishi_echonet'
and therefore this library

Thanks to Jeffro Carr who inspired me to write my own native Python ECHONET
library for Home Assistant.
Some ideas in his own repo got implemented in my own code.
(https://github.com/jethrocarr/echonetlite-hvac-mqtt-service.git)

Also big thanks to Futomi Hatano for open sourcing a well-documented ECHONET Lite
library in Node JS that formed
the basis of my reverse engineering efforts.
(https://github.com/futomi/node-echonet-lite)

## License

This application is licensed under an MIT license, refer to LICENSE for details.

***
[pychonet]: https://github.com/scottyphillips/pychonet
[releases-shield]: https://img.shields.io/github/release/scottyphillips/pychonet.svg?style=for-the-badge
[releases]: https://github.com/scottyphillips/pychonet/releases
[license-shield]:https://img.shields.io/github/license/scottyphillips/pychonet?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/RgKWqyt?style=for-the-badge
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/Maintainer-Scott%20Phillips-blue?style=for-the-badge
