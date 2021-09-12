from pychonet.echonetapiclient import ECHONETAPIClient
from .EchonetInstance import EchonetInstance
from .HomeAirConditioner import HomeAirConditioner
from .HomeSolarPower import HomeSolarPower
from .ElectricVehicleCharger import ElectricVehicleCharger
from .StorageBattery import StorageBattery
from .TemperatureSensor import TemperatureSensor
from pychonet.lib.eojx import EOJX_CLASS

def Factory(host, server, eojgc, eojcc, eojci= 0x01):

    instance = EOJX_CLASS[eojgc][eojcc]

    """Factory Method"""
    instances = {
        'Home air conditioner': HomeAirConditioner,
        'Home solar power generation': HomeSolarPower,
        'Electric vehicle charger/discharger': ElectricVehicleCharger,
        'Temperature sensor': TemperatureSensor,
        'Storage Battery': StorageBattery
    }
    instance_object = instances.get(instance, None)
    if instance_object is not None:
        return instance_object(host, server, eojci)

    return EchonetInstance(host, server, eojgc, eojcc, eojci)
