
from pychonet.echonetapiclient import ECHONETAPIClient  # noqa
from pychonet.lib.eojx import EOJX_CLASS

from .version import __version__
from .AutomaticEntranceDoor import AutomaticEntranceDoor
from .BathroomDryer import BathroomDryer
from .CeilingFan import CeilingFan
from .CO2Sensor import CO2Sensor
from .GasSensor import GasSensor
from .DistributionPanelMeter import DistributionPanelMeter
from .EchonetInstance import EchonetInstance
from .ElectricBlind import ElectricBlind
from .ElectricCurtain import ElectricCurtain
from .ElectricEnergyMeter import ElectricEnergyMeter
from .ElectricGate import ElectricGate
from .ElectricHeater import ElectricHeater
from .ElectricLock import ElectricLock
from .ElectricRainSlidingDoor import ElectricRainSlidingDoor
from .ElectricShutter import ElectricShutter
from .ElectricStorageHeater import ElectricStorageHeater
from .ElectricVehicleCharger import ElectricVehicleCharger
from .ElectricVehicleChargerDischarger import ElectricVehicleChargerDischarger
from .ElectricWaterHeater import ElectricWaterHeater
from .ElectricWindow import ElectricWindow
from .FanHeater import FanHeater
from .FireSensor import FireSensor
from .FloorHeater import FloorHeater
from .FuelCell import FuelCell
from .FrequencyRegulation import FrequencyRegulation
from .FirstAidSensor import FirstAidSensor
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
from .RiceCooker import RiceCooker
from .SingleFunctionLighting import SingleFunctionLighting
from .StorageBattery import StorageBattery
from .HumiditySensor import HumiditySensor
from .TemperatureSensor import TemperatureSensor
from .WaterFlowMeter import WaterFlowMeter
from .DistributedGeneratorElectricEnergyMeter import DistributedGeneratorElectricEnergyMeter
from .Electricthermos import ElectricThermos
from .CrimeSensor import CrimeSensor
from .EmergencyButton import EmergencyButton
from .CigaretteSensor import CigaretteSensor
from .VO2Sensor import VO2Sensor
from .DiffPressureSensor import DiffPressureSensor
from .AirSpeedSensor import AirSpeedSensor
from .FlameSensor import FlameSensor
from .WaterFlowSensor import WaterFlowSensor
from .OdorSensor import OdorSensor
from .ElectricEnergySensor import ElectricEnergySensor
from .CurrentSensor import CurrentSensor
from .BedPresenceSensor import BedPresenceSensor
from .MicromotionSensor import MicromotionSensor
from .PassageSensor import PassageSensor
from .OpenCloseSensor import OpenCloseSensor
from .ActivityAmountSensor import ActivityAmountSensor
from .HumanDetectionSensor import HumanDetectionSensor
from .RainSensor import RainSensor
from .VisitorSensor import VisitorSensor
from .CommercialShowcase import CommercialShowcase
from .DistributionPanelMeterController import DistributionPanelMeterController
from .CombinationMicrowaveOven import CombinationMicrowaveOven


_DEVICE_CLASSES = {
    (0x00, 0x02): CrimeSensor,
    (0x00, 0x03): EmergencyButton,
    (0x00, 0x04): FirstAidSensor,
    (0x00, 0x07): HumanDetectionSensor,
    (0x00, 0x08): VisitorSensor,
    (0x00, 0x11): TemperatureSensor,
    (0x00, 0x12): HumiditySensor,
    (0x00, 0x13): RainSensor,
    (0x00, 0x19): FireSensor,
    (0x00, 0x1A): CigaretteSensor,
    (0x00, 0x1B): CO2Sensor,
    (0x00, 0x1C): GasSensor,
    (0x00, 0x1D): VO2Sensor,
    (0x00, 0x1E): DiffPressureSensor,
    (0x00, 0x1F): AirSpeedSensor,
    (0x00, 0x20): OdorSensor,
    (0x00, 0x21): FlameSensor,
    (0x00, 0x22): ElectricEnergySensor,
    (0x00, 0x23): CurrentSensor,
    (0x00, 0x25): WaterFlowSensor,
    (0x00, 0x26): MicromotionSensor,
    (0x00, 0x27): PassageSensor,
    (0x00, 0x28): BedPresenceSensor,
    (0x00, 0x29): OpenCloseSensor,
    (0x00, 0x2A): ActivityAmountSensor,
    (0x01, 0x30): HomeAirConditioner,
    (0x01, 0x35): HomeAirCleaner,
    (0x01, 0x3A): CeilingFan,
    (0x01, 0x42): ElectricHeater,
    (0x01, 0x43): FanHeater,
    (0x01, 0x55): ElectricStorageHeater,
    (0x02, 0x60): ElectricBlind,
    (0x02, 0x61): ElectricShutter,
    (0x02, 0x62): ElectricCurtain,
    (0x02, 0x63): ElectricRainSlidingDoor,
    (0x02, 0x64): ElectricGate,
    (0x02, 0x65): ElectricWindow,
    (0x02, 0x66): AutomaticEntranceDoor,
    (0x02, 0x6B): ElectricWaterHeater,
    (0x02, 0x6F): ElectricLock,
    (0x02, 0x72): HotWaterGenerator,
    (0x02, 0x73): BathroomDryer,
    (0x02, 0x79): HomeSolarPower,
    (0x02, 0x7B): FloorHeater,
    (0x02, 0x7C): FuelCell,
    (0x02, 0x7D): StorageBattery,
    (0x02, 0x7E): ElectricVehicleChargerDischarger,
    (0x02, 0x80): ElectricEnergyMeter,
    (0x02, 0x81): WaterFlowMeter,
    (0x02, 0x82): GasMeter,
    (0x02, 0x87): DistributionPanelMeter,
    (0x02, 0x88): LowVoltageSmartElectricEnergyMeter,
    (0x02, 0x8E): DistributedGeneratorElectricEnergyMeter,
    (0x02, 0x90): GeneralLighting,
    (0x02, 0x91): SingleFunctionLighting,
    (0x02, 0xA1): ElectricVehicleCharger,
    (0x02, 0xA3): LightingSystem,
    (0x02, 0xA5): MultipleInputPCS,
    (0x02, 0xA6): HybridWaterHeater,
    (0x02, 0xA7): FrequencyRegulation,
    (0x03, 0xB2): ElectricThermos,
    (0x03, 0xB7): Refrigerator,
    (0x03, 0xB8): CombinationMicrowaveOven,
    (0x03, 0xBB): RiceCooker,
    (0x03, 0xCE): CommercialShowcase,
    (0x05, 0xFF): DistributionPanelMeterController,
}


def Factory(host, server, eojgc, eojcc, eojci=0x01):
    """Create the device class for the requested EOJ or a generic instance."""
    device_class = _DEVICE_CLASSES.get((eojgc, eojcc))
    if device_class is not None:
        return device_class(host, server, eojci)
    return EchonetInstance(host, eojgc, eojcc, eojci, server)
