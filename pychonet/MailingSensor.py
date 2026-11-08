from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF, DICT_31_8_LEVELS


class MailingSensor(EchonetInstance):
    """ECHONET mailing sensor (Appendix section 3.1.15)."""

    EPC_FUNCTIONS = {
        0x80: [_int, DICT_30_ON_OFF],  # Operation status
        0xB0: [_int, DICT_31_8_LEVELS],  # Detection threshold level
        0xB1: [_int, {0x41: "found", 0x42: "not found"}],  # Mailing detection status
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        super().__init__(host, 0x00, 0x0F, instance, api_connector)

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getDetectionThresholdLevel(self):
        return await self.getMessage(0xB0)

    async def setDetectionThresholdLevel(self, level):
        return await self.setMessage(0xB0, level)

    async def getMailingDetectionStatus(self):
        return await self.getMessage(0xB1)
