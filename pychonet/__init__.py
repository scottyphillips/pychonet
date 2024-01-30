from pychonet.echonetapiclient import ECHONETAPIClient  # noqa
from pychonet.lib.eojx import EOJX_CLASS

from .version import __version__
from .EchonetInstance import EchonetInstance
from .ElectricBlind import ElectricBlind
from .ElectricShutter import ElectricShutter
from .ElectricCurtain import ElectricCurtain
from .ElectricRainSlidingDoor import ElectricRainSlidingDoor
from .ElectricGate import ElectricGate
from .ElectricWindow import ElectricWindow
from .AutomaticEntranceDoor import AutomaticEntranceDoor
from .ElectricLock import ElectricLock
from .ElectricVehicleCharger import ElectricVehicleCharger
from .GeneralLighting import GeneralLighting
from .SingleFunctionLighting import SingleFunctionLighting
from .LightingSystem import LightingSystem
from .HomeAirCleaner import HomeAirCleaner
from .HomeAirConditioner import HomeAirConditioner
from .HomeSolarPower import HomeSolarPower
from .StorageBattery import StorageBattery
from .TemperatureSensor import TemperatureSensor
from .DistributionPanelMeter import DistributionPanelMeter
from .LowVoltageSmartElectricEnergyMeter import LowVoltageSmartElectricEnergyMeter
from .HybridWaterHeater import HybridWaterHeater
from .HotWaterGenerator import HotWaterGenerator
from .FloorHeater import FloorHeater
from .FuelCell import FuelCell
from .GasMeter import GasMeter
from .ElectricEnergyMeter import ElectricEnergyMeter
from .WaterFlowMeter import WaterFlowMeter
from .CeilingFan import CeilingFan
from .ElectricWaterHeater import ElectricWaterHeater


def Factory(host, server, eojgc, eojcc, eojci=0x01):
    instance = None
    if eojgc in EOJX_CLASS:
        if eojcc in EOJX_CLASS[eojgc]:
            instance = f"{eojgc}-{eojcc}"

    """Factory Method"""
    instances = {
        f"{0x00}-{0x11}": TemperatureSensor,
        f"{0x01}-{0x30}": HomeAirConditioner,
        f"{0x01}-{0x35}": HomeAirCleaner,
        f"{0x01}-{0x3A}": CeilingFan,
        f"{0x02}-{0x60}": ElectricBlind,
        f"{0x02}-{0x61}": ElectricShutter,
        f"{0x02}-{0x62}": ElectricCurtain,
        f"{0x02}-{0x63}": ElectricRainSlidingDoor,
        f"{0x02}-{0x64}": ElectricGate,
        f"{0x02}-{0x65}": ElectricWindow,
        f"{0x02}-{0x66}": AutomaticEntranceDoor,
        f"{0x02}-{0x6B}": ElectricWaterHeater,
        f"{0x02}-{0x6F}": ElectricLock,
        f"{0x02}-{0x72}": HotWaterGenerator,
        f"{0x02}-{0x79}": HomeSolarPower,
        f"{0x02}-{0x7B}": FloorHeater,
        f"{0x02}-{0x7C}": FuelCell,
        f"{0x02}-{0x7D}": StorageBattery,
        f"{0x02}-{0x7E}": ElectricVehicleCharger,
        f"{0x02}-{0x80}": ElectricEnergyMeter,
        f"{0x02}-{0x81}": WaterFlowMeter,
        f"{0x02}-{0x82}": GasMeter,
        f"{0x02}-{0x87}": DistributionPanelMeter,
        f"{0x02}-{0x88}": LowVoltageSmartElectricEnergyMeter,
        f"{0x02}-{0x90}": GeneralLighting,
        f"{0x02}-{0x91}": SingleFunctionLighting,
        f"{0x02}-{0xA3}": LightingSystem,
        f"{0x02}-{0xA6}": HybridWaterHeater,
        None: None,
    }
    instance_object = instances.get(instance, None)
    if instance_object is not None:
        return instance_object(host, server, eojci)

    return EchonetInstance(host, eojgc, eojcc, eojci, server)
