from typing import Dict
from pychonet.EchonetInstance import EchonetInstance
from pychonet.GeneralLighting import ENL_BRIGHTNESS
from pychonet.lib.const import EFFECT_OFF, ENL_STATUS
from pychonet.lib.epc_functions import _int

ENL_SCENE = 0xC0
ENL_SCENE_MAX = 0xC1


class LightingSystem(EchonetInstance):
    EPC_FUNCTIONS = {
        0xB0: _int,  # Illuminance level setting
        0xC0: _int,  # Scene control setting
        0xC1: _int,  # Max scene control setting
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02  # Housing/facility-related device group
        self._eojcc = 0xA3  # Lighting System class
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    """
    getBrightness get the brightness that has been set in the light

    return: A string representing the configured brightness.
    """

    async def getBrightness(self):
        return await self.getMessage(ENL_BRIGHTNESS)  # ['brightness']

    """
    setBrightness set the temperature of the light

    param temperature: A string representing the desired temperature.
    """

    async def setBrightness(self, brightness):
        return await self.setMessage(ENL_BRIGHTNESS, int(brightness))

    """
    setLightStates set the light states

    param status: A Dict any light states
    """

    async def setLightStates(self, states: Dict):
        status = states.get("status")
        brightness = states.get("brightness")
        effect = states.get("effect")

        opc = list()

        if status is not None:
            opc.append({"EPC": ENL_STATUS, "PDC": 0x01, "EDT": int(status)})
        if brightness is not None:
            opc.append({"EPC": ENL_BRIGHTNESS, "PDC": 0x01, "EDT": int(brightness)})
        if effect is not None:
            if effect == EFFECT_OFF:
                scean_num = 0
            else:
                scean_num = effect.split()[1]
            opc.append({"EPC": ENL_SCENE, "PDC": 0x01, "EDT": int(scean_num)})
        return await self.setMessages(opc)

    def getEffectList(self):
        """Get Effect List

        Returns:
            list|None: Effect list or None
        """
        if (max_num := self._epc_data.get(ENL_SCENE_MAX)) != None:
            effect_list = [EFFECT_OFF]
            for i in range(1, _int(max_num) + 1):
                effect_list.append("scene " + str(i))
            return effect_list
        return None

    def getEffect(self):
        """Get Current Effect

        Returns:
            string: Value of current effect
        """
        if scean_num := self._epc_data.get(ENL_SCENE):
            return "scene " + str(_int(scean_num))
        return EFFECT_OFF
