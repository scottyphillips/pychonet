from pychonet.echonetapiclient import ECHONETAPIClient
from .EchonetInstance import EchonetInstance
from .HomeAirConditioner import HomeAirConditioner

def Factory(instance, host, server, eojci= 0x01):

    """Factory Method"""
    instances = {
        "EchonetInstance": EchonetInstance,
        "HomeAirConditioner": HomeAirConditioner,
    }

    return instances[instance](host, server, eojci)
