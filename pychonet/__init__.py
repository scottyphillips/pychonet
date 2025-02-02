from pychonet.echonetapiclient import ECHONETAPIClient  # noqa
from pychonet.lib.eojx import EOJX_CLASS

from .version import __version__
from .AutomaticEntranceDoor import AutomaticEntranceDoor
from .BathroomDryer import BathroomDryer
from .CeilingFan import CeilingFan
from .DistributionPanelMeter import DistributionPanelMeter
from .EchonetInstance import EchonetInstance
from .ElectricBlind import ElectricBlind
from .ElectricCurtain import ElectricCurtain
from .ElectricEnergyMeter import ElectricEnergyMeter
from .ElectricGate import ElectricGate
from .ElectricLock import ElectricLock
from .ElectricRainSlidingDoor import ElectricRainSlidingDoor
from .ElectricShutter import ElectricShutter
from .ElectricVehicleCharger import ElectricVehicleCharger
from .ElectricWaterHeater import ElectricWaterHeater
from .ElectricWindow import ElectricWindow
from .FloorHeater import FloorHeater
from .FuelCell import FuelCell
from .GasMeter import GasMeter
from .GeneralLighting import GeneralLighting
from .HomeAirCleaner import HomeAirCleaner
from .HomeAirConditioner import HomeAirConditioner
from .HomeSolarPower import HomeSolarPower
from .HotWaterGenerator import HotWaterGenerator
from .HybridWaterHeater import HybridWaterHeater
from .LightingSystem import LightingSystem
from .MultipleInputPCS import MultipleInputPCS
from .LowVoltageSmartElectricEnergyMeter import LowVoltageSmartElectricEnergyMeter
from .Refrigerator import Refrigerator
from .SingleFunctionLighting import SingleFunctionLighting
from .StorageBattery import StorageBattery
from .TemperatureSensor import TemperatureSensor
from .WaterFlowMeter import WaterFlowMeter


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
        f"{0x02}-{0x73}": BathroomDryer,
        f"{0x02}-{0x79}": HomeSolarPower,
        f"{0x02}-{0x7B}": FloorHeater,
        f"{0x02}-{0x7C}": FuelCell,
        f"{0x02}-{0x7D}": StorageBattery,
        # f"{0x02}-{0x7E}": ElectricVehicleCharger,
        f"{0x02}-{0x80}": ElectricEnergyMeter,
        f"{0x02}-{0x81}": WaterFlowMeter,
        f"{0x02}-{0x82}": GasMeter,
        f"{0x02}-{0x87}": DistributionPanelMeter,
        f"{0x02}-{0x88}": LowVoltageSmartElectricEnergyMeter,
        f"{0x02}-{0x90}": GeneralLighting,
        f"{0x02}-{0x91}": SingleFunctionLighting,
        f"{0x02}-{0xA3}": LightingSystem,
        f"{0x02}-{0xA5}": MultipleInputPCS,
        f"{0x02}-{0xA6}": HybridWaterHeater,
        f"{0x03}-{0xB7}": Refrigerator,
        None: None,
    }
    instance_object = instances.get(instance, None)
    if instance_object is not None:
        return instance_object(host, server, eojci)

    return EchonetInstance(host, eojgc, eojcc, eojci, server)
