# tests/test_rice_cooker.py
import unittest
from pychonet.RiceCooker import RiceCooker


class MockECHONETAPIClient:
    def __init__(self):
        # Raw byte values that simulate device responses
        # _hh_mm() format: hh = int(edt[0]), mm = str(int(edt[1])).zfill(2)
        # So b'\x00\x00' -> "0:00", b'\x05\x00' -> "5:00"
        # DICT_30_OPEN_CLOSED: 0x30 = "open", 0x31 = "closed"
        self._state = {
            "192.168.1.100": {
                "instances": {
                    0x03: {  # Group code for Rice Cooker
                        0xBB: {  # Class code for Rice Cooker
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF (DICT_30_ON_OFF[0x31] = "off")
                                0xB0: b'\x30',  # Cover status: Open (DICT_30_OPEN_CLOSED[0x30] = "open")
                                0xB1: b'\x42',  # Rice cooking status: Cooking in progress
                                0xB2: b'\x41',  # Control setting: Start/Restart
                                0xE1: b'\x42',  # Warmer setting: Off (DICT_41_ON_OFF[0x42] = "off")
                                0xE5: b'\x41',  # Inner pot removal: Installed
                                0xE6: b'\x41',  # Cover removal: Installed
                                0x90: b'\x42',  # Reservation setting: Off (DICT_41_ON_OFF[0x42] = "off")
                                0x91: b'\x00\x00',  # Reservation time: 0:00 (hh:mm format)
                                0x92: b'\x00\x00',  # Reservation relative time: 0:00 (hh:mm format)
                                0x9F: [0x80, 0xB0, 0xB1, 0xB2, 0xE1, 0xE5, 0xE6, 0x90],  # GETMAP
                                0x9E: [0x80, 0xB0, 0xB1, 0xB2, 0xE1, 0xE5, 0xE6, 0x90],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        # Simulate a successful response
        return True


class TestRiceCooker(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        status = await rc.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF (DICT_30_ON_OFF[0x31] = "off")

        status = await rc.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = "off"
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        result = await rc.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getCoverStatus(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        cover_status = await rc.getCoverStatus()
        self.assertEqual(cover_status, b'\x30')  # Open (DICT_30_OPEN_CLOSED[0x30] = "open")
        status = await rc.update(0xB0)
        expected = 'open'  # DICT_30_OPEN_CLOSED[0x30] = "open"
        self.assertEqual(status, expected)

    async def test_getRiceCookingStatus(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        cooking_status = await rc.getRiceCookingStatus()
        self.assertEqual(cooking_status, b'\x42')  # Cooking in progress
        status = await rc.update(0xB1)
        expected = 'Rice cooking in progress'  # DICT_30_ON_OFF[0x42] = 'Rice cooking in progress'
        self.assertEqual(status, expected)

    async def test_getRiceCookingControlSetting(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        control_setting = await rc.getRiceCookingControlSetting()
        self.assertEqual(control_setting, b'\x41')  # Start/Restart
        status = await rc.update(0xB2)
        expected = 'Start/Restart'  # DICT_41_ON_OFF[0x41] = 'Start/Restart'
        self.assertEqual(status, expected)

    async def test_setRiceCookingControlSetting(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        result = await rc.setRiceCookingControlSetting('pause')
        self.assertTrue(result)

    async def test_getWarmerSetting(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        warmer_setting = await rc.getWarmerSetting()
        self.assertEqual(warmer_setting, b'\x42')  # Off (DICT_41_ON_OFF[0x42] = "off")
        status = await rc.update(0xE1)
        expected = 'off'  # DICT_41_ON_OFF[0x42] = "off"
        self.assertEqual(status, expected)

    async def test_setWarmerSetting(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        result = await rc.setWarmerSetting('on')
        self.assertTrue(result)

    async def test_getInnerPotRemovalStatus(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        inner_pot_status = await rc.getInnerPotRemovalStatus()
        self.assertEqual(inner_pot_status, b'\x41')  # Installed
        status = await rc.update(0xE5)
        expected = 'Installed'  # {0x41: "Installed", 0x42: "Removed"}
        self.assertEqual(status, expected)

    async def test_getCoverRemovalStatus(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        cover_removal_status = await rc.getCoverRemovalStatus()
        self.assertEqual(cover_removal_status, b'\x41')  # Installed
        status = await rc.update(0xE6)
        expected = 'Installed'  # {0x41: "Installed", 0x42: "Removed"}
        self.assertEqual(status, expected)

    async def test_getRiceCookingReservationSetting(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        reservation_setting = await rc.getRiceCookingReservationSetting()
        self.assertEqual(reservation_setting, b'\x42')  # Off (DICT_41_ON_OFF[0x42] = "off")
        status = await rc.update(0x90)
        expected = 'off'  # DICT_41_ON_OFF[0x42] = "off"
        self.assertEqual(status, expected)

    async def test_setRiceCookingReservationSetting(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        result = await rc.setRiceCookingReservationSetting('on')
        self.assertTrue(result)

    async def test_getRiceCookingReservationSettingTime(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        reservation_time = await rc.getRiceCookingReservationSettingTime()
        # _hh_mm() returns "0:00" for b'\x00\x00' (hh={int(edt[0])}, mm=st(int(edt[1])).zfill(2))
        self.assertEqual(reservation_time, b'\x00\x00')  # 0:00 hours:minutes

        status = await rc.update(0x91)
        expected = '0:00'  # _hh_mm() format: f"{hh}:{mm}"
        self.assertEqual(status, expected)

    async def test_setRiceCookingReservationSettingTime(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        result = await rc.setRiceCookingReservationSettingTime(180)  # 3 hours
        self.assertTrue(result)

    async def test_getRiceCookingReservationSettingRelativeTime(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        relative_time = await rc.getRiceCookingReservationSettingRelativeTime()
        # _hh_mm() returns "0:00" for b'\x00\x00' (hh={int(edt[0])}, mm=st(int(edt[1])).zfill(2))
        self.assertEqual(relative_time, b'\x00\x00')  # 0:00 hours:minutes

        status = await rc.update(0x92)
        expected = '0:00'  # _hh_mm() format: f"{hh}:{mm}"
        self.assertEqual(status, expected)

    async def test_setRiceCookingReservationSettingRelativeTime(self):
        api_connector = MockECHONETAPIClient()
        rc = RiceCooker("192.168.1.100", api_connector)

        result = await rc.setRiceCookingReservationSettingRelativeTime(30)  # 30 minutes
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()