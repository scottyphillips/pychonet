# Pychonet API Reference

Complete API documentation for the pychonet ECHONETlite library.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Base Class: EchonetInstance](#base-class-echonetinstance)
3. [Device Classes](#device-classes)
   - [HomeAirConditioner](#homeairconditioner)
   - [StorageBattery](#storagebattery)
4. [EPC Functions Reference Appendix](#epc-functions-reference-appendix)

---

## Architecture Overview

### Byte Code and Data Processing Model

The library operates on ECHONET byte codes at the protocol level. Understanding this model is critical for correct usage:

| Method | Byte Code Handling | Return Value |
|--------|-------------------|--------------|
| `getMessage(EPC)` / individual getters | Raw EPC request only | Raw bytes (EDT) - no processing |
| `setMessage(EPC, EDT)` / set methods | Raw EPC set operation | Accepts byte values for parameter |
| `update([EPCs])` | Requests + invokes class-specific `EPC_FUNCTIONS` | Processed strings where functions exist, raw hex otherwise |

### Key Principles

1. **All property access uses EPC byte codes** (e.g., `0x80`, `0xB0`)
2. **set*() methods require raw byte values**, NOT string names:
   ```python
   await aircon.setMode(0x42)  # Correct - byte code for 'cool'
   # await aircon.setMode('cool')  # INCORRECT - will fail
   ```
3. **`update()` invokes EPC_FUNCTIONS** for automatic value processing:
   ```python
   result = await aircon.update([0x80, 0xB0])
   # Returns: {'128': 'On', '176': 'cool'} (processed strings)
   ```

### Device Identification

Each device type is identified by two codes:
- **EOJGC** (End Object Group Code): Device group (e.g., `0x01` = Air conditioner-related)
- **EOJCC** (End Object Class Code): Specific device class (e.g., `0x30` = Home air conditioner)

---

## Base Class: EchonetInstance

The base class for all ECHONET devices. Provides raw protocol communication methods.

### Constructor

```python
EchonetInstance(host, eojgc, eojcc, instance, api_connector=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `host` | str | IP address of the device node |
| `eojgc` | int | End Object Group Code (device group) |
| `eojcc` | int | End Object Class Code (specific class) |
| `instance` | int | Instance ID (typically 0x1) |
| `api_connector` | object | API connector for state management |

### Core Methods

#### `getMessage(epc, pdc=0x00)`
Fire a single ECHONET GET request. Returns raw bytes without processing.

```python
async def getMessage(self, epc: int, pdc: int = 0x00) -> bytes
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `epc` | int | EPC (Property) byte code to request |
| `pdc` | int | PDC (Parameter Data Control) value, default 0x00 |

**Returns:** Raw bytes (EDT payload) or False on failure

#### `setMessage(epc, edt, pdc=0x01)`
Fire a single ECHONET SET request. Requires byte values.

```python
async def setMessage(self, epc: int, edt: int, pdc: int = 0x01) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `epc` | int | EPC (Property) byte code to set |
| `edt` | int | EDT (Expected Data Type) byte value |
| `pdc` | int | PDC value, default 0x01 |

**Returns:** True if successful, False otherwise

#### `setMessages(opc)`
Fire multiple ECHONET SET requests in a single operation.

```python
async def setMessages(self, opc: list) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `opc` | list | List of dicts with 'EPC', 'PDC', 'EDT' keys |

**Returns:** True if successful, False otherwise

#### `update(attributes=None, no_request=False)`
Request multiple properties and invoke EPC_FUNCTIONS for processing.

```python
async def update(self, attributes: list = None, no_request: bool = False) -> dict | any
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `attributes` | list[int] | List of EPC codes to fetch (or single int). If None, fetches all get properties |
| `no_request` | bool | If True, returns cached data without network request |

**Returns:** 
- Single value if one attribute requested and processed
- Dict mapping EPC codes to values: `{epc: processed_value_or_hex}`
- Raw hex bytes for EPCs without defined functions

#### `getSetProperties()`
Get the settable properties map (EPC 0x9E).

```python
def getSetProperties() -> list[int]
```

**Returns:** List of EPC codes that can be set on this device

#### `getGetProperties()`
Get the readable properties map (EPC 0x9F).

```python
def getGetProperties() -> list[int]
```

**Returns:** List of EPC codes that can be read from this device

#### `getAllPropertyMaps()`
Populate the property maps for a device instance.

```python
async def getAllPropertyMaps() -> dict
```

---

## Device Classes

### HomeAirConditioner

ECHONET Home Air Conditioner (EOJGC=0x01, EOJCC=0x30)

**Byte Code Usage:**
- All property access uses EPC byte codes
- set*() methods require raw byte values, NOT string names  
- update() invokes EPC_FUNCTIONS for processed return values

#### EPC Property Table

| EPC | Name | Byte Values | Type | Access | Mandated | Announced |
|-----|------|-------------|------|--------|----------|-----------|
| 0x80 | Operation status | 0x30=ON, 0x31=OFF | u_char | R/W | O | O |
| 0x8F | Power-saving operation setting | 0x41=Saving, 0x42=Normal | u_char | R/W | O | O |
| 0xA0 | Air flow rate setting | 0x41=Auto, 0x31-0x38=Levels | u_char | R/W | O | O |
| 0xA1 | Automatic control of air flow direction | 0x41=Auto, 0x42=Non-auto, 0x43=Vert, 0x44=Horiz | u_char | R/W | - | - |
| 0xA4 | Air flow direction (vertical) setting | 0x41=Up, 0x44=L-Up, 0x43=Cent, 0x45=L-Dn, 0x42=Dn | u_char | R/W | - | - |
| 0xB0 | Operation mode setting | 0x41=Auto, 0x42=Cool, 0x43=Heat, 0x44=Dry | u_char | R/W | O | O |
| 0xB2 | Normal/High-speed/Silent op. setting | 0x41=Normal, 0x42=High-speed, 0x43=Silent | u_char | R/W | - | - |
| 0xB3 | Set temperature value | 0x00-0x32 (0-50°C) | u_char | R/W | O | - |
| 0xBB | Measured value of room temperature | 0x81-0x7D (-127 to 125°C) | s_char | R | O | - |

#### Methods

##### `getOperationalTemperature()`
Get the configured target temperature.

```python
async def getOperationalTemperature() -> dict[str, int]
```

**Returns:** `{'set_temperature': <int>}` or raw bytes if no EPC function

##### `setOperationalTemperature(temperature)`
Set the target temperature. Requires byte value (0-50 maps to 0x00-0x32).

```python
async def setOperationalTemperature(self, temperature: int) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | int | Temperature in °C (0-50), converted to byte 0x00-0x32 |

##### `getMode()`
Get the current operation mode. Returns raw bytes.

```python
async def getMode() -> dict[str, str]
```

**Returns:** Raw EPC response (processed by update() if needed)

##### `setMode(mode)`
Set operation mode. **Requires byte value**, not string name.

```python
async def setMode(self, mode: int) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `mode` | int | Byte code: 0x41=auto, 0x42=cool, 0x43=heat, 0x44=dry, 0x45=fan_only, 0x40=other, 0xFF=off |

**Note:** If mode is 'off', sets operation status to OFF. Otherwise, turns ON and sets mode.

##### `getFanSpeed()`
Get current fan speed (EPC 0xA0). Returns raw bytes.

```python
async def getFanSpeed() -> dict[str, str]
```

**Returns:** Raw EPC response

##### `setFanSpeed(fan_speed)`
Set fan speed. **Requires byte value**, not string name.

```python
async def setFanSpeed(self, fan_speed: int) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `fan_speed` | int | Byte code mapping (see FAN_SPEED dict in source):<br>0x41=auto, 0x31=minimum, 0x32=low, 0x33=medium-low,<br>0x34=medium, 0x35=medium-high, 0x36=high, 0x37=very-high, 0x38=max |

##### `getSwingMode()`
Get swing mode setting. Returns raw bytes.

```python
async def getSwingMode() -> dict[str, str]
```

**Returns:** Raw EPC response (EPC 0xA3)

##### `setSwingMode(swing_mode)`
Set automatic swing mode. **Requires byte value**.

```python
async def setSwingMode(self, swing_mode: int) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `swing_mode` | int | Byte code: 0x31=not-used, 0x41=vert, 0x42=horiz, 0x43=vert-horiz |

##### `getAutoDirection()`
Get automatic direction mode. Returns raw bytes.

```python
async def getAutoDirection() -> dict[str, str]
```

**Returns:** Raw EPC response (EPC 0xA1)

##### `setAutoDirection(auto_direction)`
Set automatic direction mode. **Requires byte value**.

```python
async def setAutoDirection(self, auto_direction: int) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `auto_direction` | int | Byte code: 0x41=auto, 0x42=non-auto, 0x43=auto-vert, 0x44=auto-horiz |

##### `getAirflowVert()`
Get vertical vane setting. Returns raw bytes.

```python
async def getAirflowVert() -> dict[str, str]
```

**Returns:** Raw EPC response (EPC 0xA4)

##### `setAirflowVert(airflow_vert)`
Set vertical vane position. **Requires byte value**.

```python
async def setAirflowVert(self, airflow_vert: int) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `airflow_vert` | int | Byte code: 0x41=upper, 0x44=upper-central, 0x43=central,<br>0x45=lower-central, 0x42=lower |

##### `getAirflowHoriz()`
Get horizontal vane setting. Returns raw bytes.

```python
async def getAirflowHoriz() -> dict[str, str]
```

**Returns:** Raw EPC response (EPC 0xA5)

##### `setAirflowHoriz(airflow_horiz)`
Set horizontal vane position. **Requires byte value**.

```python
async def setAirflowHoriz(self, airflow_horiz: int) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `airflow_horiz` | int | Byte code for positions (see AIRFLOW_HORIZ dict in source):<br>0x41=rc-right, 0x42=left-lc, 0x43=lc-center-rc, etc. |

##### `getSilentMode()`
Get fan silent mode setting. Returns raw bytes.

```python
async def getSilentMode() -> dict[str, str]
```

**Returns:** Raw EPC response (EPC 0xB2)

##### `setSilentMode(mode)`
Set normal/high-speed/silent operation mode. **Requires byte value**.

```python
async def setSilentMode(self, mode: int) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `mode` | int | Byte code: 0x41=normal, 0x42=high-speed, 0x43=silent |

##### `getRoomTemperature()`
Get measured room temperature. Returns raw bytes.

```python
async def getRoomTemperature() -> dict[str, int]
```

**Returns:** Raw EPC response (EPC 0xBB)

##### `getOutdoorTemperature()`
Get outdoor temperature reading. Returns raw bytes.

```python
async def getOutdoorTemperature() -> dict[str, int]
```

**Returns:** Raw EPC response (EPC 0xBE)

---

### StorageBattery

ECHONET Storage Battery (EOJGC=0x02, EOJCC=0x7D)

#### EPC Property Table

| EPC | Name | Byte Values | Type | Access |
|-----|------|-------------|------|--------|
| 0x80 | Operation status | 0x30=ON, 0x31=OFF | u_char | R/W |
| 0xA0 | AC effective capacity (charging) | - | int | R |
| 0xA1 | AC effective capacity (discharging) | - | int | R |
| 0xA2 | AC chargeable capacity | - | int | R |
| 0xA3 | AC dischargeable capacity | - | int | R |
| 0xA4 | AC chargeable electric energy | - | int | R |
| 0xA5 | AC dischargeable electric energy | - | int | R |
| 0xA6 | AC charge upper limit setting | - | int | R/W |
| 0xA7 | AC discharge lower limit setting | - | int | R/W |
| 0xC1 | Charging method | 0x01=maximum, 0x02=surplus,<br>0x03=designatedPower, 0x04=designatedCurrent | int | R/O |
| 0xC8-CB | Min/max power & current | - | int | R/O |
| 0xCC-CE | Permission settings | 0x41=permitted, 0x42=prohibited | int | R/W |
| 0xCF | Working operation status | See DICT_OPERATION_MODE below | int | R/W |

**DICT_OPERATION_MODE:**
```python
{0x41: "rapidCharging", 0x42: "charging", 0x43: "discharging", 
 0x44: "standby", 0x45: "test", 0x46: "auto", 0x48: "restart",
 0x49: "capacityRecalculation", 0x40: "Other"}
```

#### Methods (Selected)

##### `getOperationStatus()` / `setOperationStatus(value)`
Get or set operation status. **Requires byte value**.

```python
async def getOperationStatus() -> dict[str, str]
async def setOperationStatus(self, value: int) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | int | Byte code: 0x30=ON, 0x31=OFF |

##### `getActualOperationMode()`
Get working operation status. Returns processed string via EPC_FUNCTIONS.

```python
async def getActualOperationMode() -> dict[str, str]
```

**Returns:** Status from DICT_OPERATION_MODE or raw bytes if unavailable

##### `setOperationMode(value)`
Set operation mode setting (EPC 0xDA). **Requires byte value**.

```python
async def setOperationMode(self, value: int) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | int | Byte code from DICT_OPERATION_MODE |

##### `getBatteryType()`
Get battery chemistry type. Returns processed string via EPC_FUNCTIONS.

```python
async def getBatteryType() -> dict[str, str]
```

**Returns:** Battery type (lithiumIon=0x04, lead=0x01, ni_mh=0x02, etc.)

##### `getInstantaneousChargingAndDischargingElectricPower()`
Get instantaneous power. Returns raw bytes (EPC 0xD3).

```python
async def getInstantaneousChargingAndDischargingElectricPower() -> dict[str, int]
```

**Returns:** Power in W AC (positive=charging, negative=discharging)

##### `resetCumulativeDischargingElectricEnergy()` / `resetCumulativeChargingElectricEnergy()`
Reset cumulative energy counters. Set-only operations.

```python
async def resetCumulativeDischargingElectricEnergy() -> bool  # EPC 0xD7
async def resetCumulativeChargingElectricEnergy() -> bool     # EPC 0xD9
```

---

## EPC Functions Reference Appendix

### Generic EPC Functions (`lib/epc_functions.py`)

| Function | Description | Input Format | Output |
|----------|-------------|--------------|--------|
| `_int(edt, values_dict)` | Convert bytes to int with optional enum mapping | bytes | str or int |
| `_signed_int(edt)` | Signed integer conversion | bytes | int (can be negative) |
| `_hh_mm(edt)` | Time HH:MM format | 2-byte array | "HH:MM" string |
| `_yyyy_mm_dd(edt)` | Date YYYY:MM:DD format | 8-byte array | "YYYY:MM:DD" string |
| `_to_string(edt)` | UTF-8 string decoding | bytes | str |

### Status Dictionaries

```python
DICT_30_ON_OFF = {0x30: 'on', 0x31: 'off'}
DICT_41_AUTO_NONAUTO = {0x41: 'auto', 0x42: 'non-auto'}
DICT_41_AUTO_8_SPEEDS = {
    0x41: 'auto', 0x31: 'minimum', 0x32: 'low', 0x33: 'medium-low',
    0x34: 'medium', 0x35: 'medium-high', 0x36: 'high', 
    0x37: 'very-high', 0x38: 'max'
}
DICT_41_PERMITTED_PROHIBITED = {0x41: 'permitted', 0x42: 'prohibited'}
```

### Class-Specific EPC_FUNCTIONS

Each device class defines `EPC_FUNCTIONS` dict mapping EPC codes to processing functions. Example:

```python
# HomeAirConditioner.EPC_FUNCTIONS[0xB3] = _signed_int  # Temperature
# StorageBattery.EPC_FUNCTIONS[0xC8] = _max_min_int     # Min/max power pair
```

When `update()` is called, it looks up the EPC in this dict and applies the function to convert raw bytes to processed values. If no entry exists, raw hex bytes are returned.

---

## Common Usage Patterns

### Pattern 1: Quick status check with processing
```python
status = await aircon.update([0x80, 0xB0])
# Returns: {'128': 'On', '176': 'cool'} (processed strings)
```

### Pattern 2: Individual raw property access
```python
raw_temp = await aircon.getMessage(0xBB)
# Returns: raw bytes, no processing
```

### Pattern 3: Setting with byte values
```python
await aircon.setMode(0x42)  # Set to 'cool' (byte 0x42)
await aircon.setFanSpeed(0x35)  # Set to 'medium-high' (byte 0x35)
```

### Pattern 4: Multiple operations in one request
```python
result = await aircon.update([0x80, 0xB3, 0xBB])
# Returns processed values where possible
```
