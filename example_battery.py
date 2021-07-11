#!/usr/bin/env python3
import pychonet
import pychonet.StorageBattery

# Discover Echonet instances
instances = pychonet.discover()
print(instances)

# create a battery instance
battery = pychonet.StorageBattery("10.0.0.1")

# return all the property maps
print(battery.getAllPropertyMaps())

print(battery.getRemainingStoredElectricity3())
print(battery.WORKING_OPERATION_STATES[battery.getWorkingOperationStatus()])
