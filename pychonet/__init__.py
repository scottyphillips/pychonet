from pychonet.echonetapiclient import ECHONETAPIClient  # noqa
from pychonet.lib.eojx import EOJX_CLASS

from .version import __version__
from .EchonetInstance import EchonetInstance
from .ElectricBlind import ElectricBlind
from .ElectricLock import ElectricLock
from .ElectricVehicleCharger import ElectricVehicleCharger
from .GeneralLighting import GeneralLighting
from .HomeAirCleaner import HomeAirCleaner
from .HomeAirConditioner import HomeAirConditioner
from .HomeSolarPower import HomeSolarPower
from .StorageBattery import StorageBattery
from .TemperatureSensor import TemperatureSensor
from .DistributionPanelMeter import DistributionPanelMeter
from .HybridWaterHeater import HybridWaterHeater
from .HotWaterGenerator import HotWaterGenerator
from .GasMeter import GasMeter
from .ElectricEnergyMeter import ElectricEnergyMeter
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
        f"{0x02}-{0x60}": ElectricBlind,
        f"{0x02}-{0x6F}": ElectricLock,
        f"{0x02}-{0x72}": HotWaterGenerator,
        f"{0x02}-{0x79}": HomeSolarPower,
        f"{0x02}-{0x7D}": StorageBattery,
        f"{0x02}-{0x7E}": ElectricVehicleCharger,
        f"{0x02}-{0x80}": ElectricEnergyMeter,
        f"{0x02}-{0x81}": WaterFlowMeter,
        f"{0x02}-{0x82}": GasMeter,
        f"{0x02}-{0x87}": DistributionPanelMeter,
        f"{0x02}-{0x90}": GeneralLighting,
        f"{0x02}-{0xA6}": HybridWaterHeater,
        None: None,
    }
    instance_object = instances.get(instance, None)
    if instance_object is not None:
        return instance_object(host, server, eojci)

    return EchonetInstance(host, eojgc, eojcc, eojci, server)
