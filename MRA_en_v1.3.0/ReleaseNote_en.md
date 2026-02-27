# MRA Release note (V1.3.0)

2024.08.02

- Data version: 1.3.0
- Data format version: 1.2.0
- Appendix Release version: R (rev.2)

The MRA supports Release R (rev.2) and adds several new device and mofifies some devices.

## Revision history

| Data version | Date       | Description                                                                                                   |
| :----------- | :--------- | :------------------------------------------------------------------------------------------------------------ |
| 1.0.0        | 2021.11.17 | Official release                                                                                                                                  |
| 1.0.1        | 2021.12.01 | Bug fixes found in validation of the device description created from MRA v1.0.0                                                                   |
| 1.1.0        | 2022.05.27 | Supports Appendix Release version N, P, P (rev.1). </br>Adds eight kinds of devices.</br>Fixes to Typo, etc. in the English version of Release P. |
| 1.2.0        | 2023.04.28 | Supports Appendix Release version Q, Q (rev.1).</br>Adds a new device.</br>                                           |
| 1.3.0        | 2023.08.02 | Supports Appendix Release version R, R (rev.2).</br>Adds five new devices.</br>                                           |

## Additional devices

The following five device objects are additionally released this time.

| EOJ    | Device name                                            |
| :----- | :----------------------------------------------------- |
| 0x0002 | Crime prevention sensor                                |
| 0x0260 | Electrically operated blind/shade                      |
| 0x02A7 | Frequency regulation                                   |
| 0x02A5 | Multiple input PCS                                     |
| 0x028F | Bidirectional high voltage smart electric energy meter |

## Some modifications

The device objects to be modified and released are the following : super classes and five models.

| EOJ    | Device name                                     |
| :----- | :---------------------------------------------- |
| 0x0000 | Super class                                     |
| 0x0263 | Electrically operated rain sliding door/shutter |
| 0x0279 | Household solar power generation                |
| 0x027D | Storage battery                                |
| 0x02A1 | EV charger                                      |
| 0x0288 | Low-voltage smart electric energy meter         |

# MRA Release note (V1.2.0)

2023.04.28

- Data version: 1.2.0
- Data format version: 1.1.0
- Appendix Release version: Q (rev.1)

The MRA supports Release Q (rev.1) and adds a new device and mofifies some devices.

## Revision history

| Data version | Date       | Description                                                                                                                                       |
| :----------- | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0.0        | 2021.11.17 | Official release                                                                                                                                  |
| 1.0.1        | 2021.12.01 | Bug fixes found in validation of the device description created from MRA v1.0.0                                                                   |
| 1.1.0        | 2022.05.27 | Supports Appendix Release version N, P, P (rev.1). </br>Adds eight kinds of devices.</br>Fixes to Typo, etc. in the English version of Release P. |
| 1.2.0        | 2023.04.28 | Supports Appendix Release version Q, Q (rev.1).</br>Adds a new device.</br>                                                                       |

## Additional devices

The following a device object is additionally released this time.

| EOJ    | Device name                                   |
| :----- | :-------------------------------------------- |
| 0x028E | distributed generator's electric energy meter |

## Some modifications

The device objects to be modified and released are the following : super classes and four models.

| EOJ    | Device name               |
| :----- | :------------------------ |
| 0x0000 | Super class               |
| 0x026B | Electric water heater     |
| 0x027E | EV charger and discharger |
| 0x0281 | Water flowmeter           |
| 0x05FF | Controller                |

# MRA Release note (V1.1.0)

2022.05.27

- Data version: 1.1.0
- Data format version: 1.1.0
- Appendix Release version: P (rev.1)

The MRA supports Release P (rev.1) and adds several new devices.

## Revision history

| Data version | Date       | Description                                                                                                                                       |
| :----------- | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0.0        | 2021.11.17 | Official release                                                                                                                                  |
| 1.0.1        | 2021.12.01 | Bug fixes found in validation of the device description created from MRA v1.0.0                                                                   |
| 1.1.0        | 2022.05.27 | Supports Appendix Release version N, P, P (rev.1). </br>Adds eight kinds of devices.</br>Fixes to Typo, etc. in the English version of Release P. |



## Additional devices

The following eight device objects are additionally released this time.

| EOJ    | Device name                                  |
| :----- | :------------------------------------------- | :-------- |
| 0x0007 | Human detection sensor                       |
| 0x0012 | Humidity sensor                              |
| 0x0016 | Bath heating status sensor                   |
| 0x001B | CO2 sensor                                   |
| 0x0281 | Water flowmeter                              |
| 0x0282 | ガスメータ                                   | Gas meter |
| 0x028D | Smart electric energy meter for sub-metering |
| 0x02A3 | Lighting system                              |

## Modification of definitions

- Added the following items to definitions
  - number_1-999
  - number_1-999999
  - number_0-999999999m3
  - state_LightColor_40-44FD
  - state_NoData_FFFE

# MRA Release note (V1.0.1)

2022.01.07

- Data version: 1.0.1
- Data format version: 1.0.0
- Appendix Release version: M

## Revision history

| Data version | Date       | Description                                                                     |
| :----------- | :--------- | :------------------------------------------------------------------------------ |
| 1.0.0        | 2021.11.17 | Official release                                                                |
| 1.0.1        | 2021.12.01 | Bug fixes found in validation of the device description created from MRA v1.0.0 |

## Some modifications

| File               | EPC  | 変更内容                                                                         |
| :----------------- | :--- | :------------------------------------------------------------------------------- |
| 0x027A_mcrule.json | 0xE7 | Corrected the position of note description                                       |
| 0x027A_mcrule.json | 0xE8 | Corrected the position of note description                                       |
| 0x027B_mcrule.json | 0xE7 | Corrected the position of note description                                       |
| 0x027B_mcrule.json | 0xE8 | Corrected the position of note description                                       |
| 0x0280_mcrule.json | 0xE0 | Added description (\*1)                                                          |
| 0x0280_mcrule.json | 0xE3 | Added description (\*1)                                                          |
| 0x03B9_mcrule.json | 0xE7 | Corrected the description of oneOf so that the correct DD is generated.          |
| 0x0290.json        | 0xBB | shortName to lightColorForMainLighting                                           |
| 0x027A.json        | 0xE7 | note changed to remark                                                           |
| 0x027A.json        | 0xE8 | note changed to remark                                                           |
| 0x0288.json        | 0xE5 | ddefinitions / state DefaultValue FF (no change in content)                      |
| 0x0602.json        | 0xB2 | Fixed name in bitmaps to match Device Descriptions (\*2)                         |
| definitions.json   |      | Corrected the value of "format" of number_-999999999--1Wh (unit32-> int32) (\*3) |

(\*1)

```
"note" : {
  "ja" : "EPC=0xE2の値を乗算済みの値",
  "en" : "The value is multipled by the value of EPC=0xE2."
}
```

(\*2)

| Before modification | After modification  |
| :------------------ | :------------------ |
| ansiX34             | ansiX34Equipped     |
| shiftJis            | shiftJisEquipped    |
| jis                 | jisEquipped         |
| japaneseEuc         | japaneseEucEquipped |
| ucs4                | ucs4Equipped        |
| ucs2                | ucs2Equipped        |
| latin1              | latin1Equipped      |
| utf8                | utf8Equipped        |

(\*3)

Before modification

```json
    "number_-999999999--1Wh": {
      "type": "number",
      "format": "uint32",
      "minimum": -999999999,
      "maximum": -1,
      "unit": "Wh"
    },
```

After modification

```json
    "number_-999999999--1Wh": {
      "type": "number",
      "format": "int32",
      "minimum": -999999999,
      "maximum": -1,
      "unit": "Wh"
    },
```

# MRA Release note (V1.0.0)

2021.12.01

- Data version: 1.0.0
- Data format version: 1.0.0
- Appendix Release version: M

The MRA data for the APPENDIX Detailed Requirements for ECHONET Device objects is released in compliance with Guidebook of Machine Readable Appendix (MRA) V1.0.0.

The following 38 device objects are released this time.

| EOJ    | Device name                                                                         |
| :----- | :---------------------------------------------------------------------------------- |
| 0x0011 | Temperature sensor                                                                  |
| 0x0022 | Electric energy sensor                                                              |
| 0x0023 | Current value sensor                                                                |
| 0x0130 | Home air conditioner                                                                |
| 0x0133 | Ventilation fan                                                                     |
| 0x0134 | Air conditioner ventilation fan                                                     |
| 0x0135 | Air cleaner                                                                         |
| 0x0156 | Package-type commercial air conditioner (indoor unit)(except those for facilities)  |
| 0x0157 | Package-type commercial air conditioner (outdoor unit)(except those for facilities) |
| 0x0263 | Electrically operated rain sliding door/shutter                                     |
| 0x026B | Electric water heater                                                               |
| 0x026F | Electric key                                                                        |
| 0x0272 | Instantaneous water heater                                                          |
| 0x0273 | Bathroom heater & dryer                                                             |
| 0x0279 | Household solar power generation                                                    |
| 0x027A | Hot water heat source equipment                                                     |
| 0x027B | Floor heater                                                                        |
| 0x027C | Fuel cell                                                                           |
| 0x027D | Storage battery                                                                     |
| 0x027E | EV charger & discharger                                                             |
| 0x0280 | Watt-hour meter                                                                     |
| 0x0287 | Power distribution board                                                            |
| 0x0288 | Low-voltage smart electric energy meter                                             |
| 0x028A | High-voltage smart electric energy meter                                            |
| 0x0290 | General lighting                                                                    |
| 0x0291 | Mono functional lighting                                                            |
| 0x02A1 | EV charger                                                                          |
| 0x02A4 | Extended lighting system                                                            |
| 0x02A6 | Hybrid water heater                                                                 |
| 0x03B7 | Refrigerator                                                                        |
| 0x03B9 | Cooking heater                                                                      |
| 0x03BB | Rice cooker                                                                         |
| 0x03CE | Commercial show case                                                                |
| 0x03D3 | Washer & dryer                                                                      |
| 0x03D4 | Commercial show case outdoor unit                                                   |
| 0x05FD | Switch                                                                              |
| 0x05FF | Controller                                                                          |
| 0x0602 | Television                                                                          |

- The data corresponding to the device object super class is described in 0x0000.json.
- The data corresponding to the node profile (0x0EF0) is described in 0x0EF0.json. It contains the contents of the profile object super class.
- History information about specification changes is written based on the contents of APPENDIX Revision History M_20211109.xls.
For electrically operated rain sliding door/shutter (0x0263), fuel cell (0x027C), electric vehicle charger/discharger (0x027E), and low-voltage smart electric energy meter (0x0288), the historical information from Release D, C, D, and F, respectively, is described in consideration of the revisions made for each release.
- The files in the folder MCRules are used to generate Device Descriptions for the ECHONET Lite Web API.
