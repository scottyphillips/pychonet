from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int

ENL_LVSEEM_COEF = 0xD3
ENL_LVSEEM_DIGITS = 0xD7
ENL_LVSEEM_ENG_UNIT = 0xE1
ENL_LVSEEM_ENG_NOR = 0xE0
ENL_LVSEEM_ENG_REV = 0xE3
ENL_LVSEEM_INSTANT_ENG = 0xE7
ENL_LVSEEM_INSTANT_CUR = 0xE8

def _0288E1(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x00: 1,
              0x01: 0.1,
              0x02: 0.01,
              0x03: 0.001,
              0x04: 0.0001,
              0x0A: 10,
              0x0B: 100,
              0x0C: 1000,
              0x0D: 10000}
    return values.get(op_mode, None)

def _0288E2(edt):
    '''
    1～2 バイト目：積算履歴収集日
    0x0000～0x0063(0～99)
    3 バイト目以降：積算電力量計測
    値
    0x00000000～0x05F5E0FF
    (0～99,999,999)
    '''
    return "Not implemented"

def _0288E8(edt):
    r_phase = float(int.from_bytes(edt[0:2], "big", signed=True)) / 10  # R Phase
    t_phase = float(int.from_bytes(edt[2:4], "big", signed=True)) / 10  # T Phase
    if t_phase == 3276.6:
        t_phase = None
    return {"r_phase_amperes": r_phase, "t_phase_amperes": t_phase}

def _0288EA(edt):
    '''
    1～４バイト目：計測年月日
    YYYY:0x0001～0x270F
    (1～9999)
    MM:0x01～0x0C(1～12)
    DD:0x01～0x1F(1～31)
    5～７バイト目：計測時刻
    ｈｈ:0x00～0x17(0～23)
    mm:0x00～0x3B(0～59)
    ss:0x00～0x3B(0～59)
    8～11 バイト目：積算電力量計測値
    0x00000000～0x05F5E0FF
    (0～99,999,999)
    '''
    return "Not implemented"

def _0288EC(edt):
    """
    1～6 バイト目：積算履歴収集日時
    YYYY:0x0001～0x270F
    (1～9999 年)
    MM:0x01～0x0C(1～12 月)
    DD:0x01～0x1F(1～31 日)
    hh:0x00～0x17(0～23 時)
    mm:0x00/0x1E(0/30 分)
    7 バイト目：収集コマ数
    0x01～0x0C(1～12 コマ)
    8 バイト目以降：
    積算電力量計測値(正方向)
    0x00000000～0x05F5E0FF
    (0～99,999,999)
    積算電力量計測値(逆方向)
    0x00000000～0x05F5E0FF
    (0～99,999,999)
    """
    return "Not implemented"

def _0288ED(edt):
    '''
    1～6 バイト目：積算履歴収集日時
    YYYY:0x0001～0x270F
    (1～9999 年)
    MM:0x01～0x0C(1～12 月)
    DD:0x01～0x1F(1～31 日)
    hh:0x00～0x17(0～23 時)
    mm:0x00/0x1E(0/30 分)
    7 バイト目：収集コマ数
    0x01～0x0C(1～12 コマ)
    8 バイト目以降：
    積算電力量計測値(正方向)
    0x00000000～0x05F5E0FF
    (0～99,999,999)
    積算電力量計測値(逆方向)
    0x00000000～0x05F5E0FF
    (0～99,999,999)
    '''
    return "Not implemented"

class LowVoltageSmartElectricEnergyMeter(EchonetInstance):
    EPC_FUNCTIONS = {
        0xD3: _int, #"Coefficient"
        0xD7: _int, #"Number of effective digits for cumulative amounts of electric energy"
        0xE0: _int, #"Measured cumulative amount of electric energy (normal direction)"
        0xE1: _0288E1, #"Unit for cumulative amounts of electric energy (normal and reverse directions)"
        # 0xE2: _0288E2, #"Historical data of measured cumulative amounts of electric energy 1 (normal direction)"
        0xE3: _int, #"Measured cumulative amounts of electric energy (reverse direction)"
        # 0xE4: _0288E2, #"Historical data of measured cumulative amounts of electric energy 1 (reverse direction)"
        # 0xE5: _int, #"Day for which the historical data of measured cumulative amounts of electric energy is to be retrieved 1"
        0xE7: _signed_int, #"Measured instantaneous electric energy"
        0xE8: _0288E8, #"Measured instantaneous currents"
        # 0xEA: _0288EA, #"Cumulative amounts of electric energy measured at fixed time (normal direction)"
        # 0xEB: _0288EA, #"Cumulative amounts of electric energy measured at fixed time (reverse direction)"
        # 0xEC: _0288EC, #"Historical data of measured cumulative amounts of electric energy 2 (normal and reverse directions)"
        # 0xED: _0288ED, #"Day for which the historical data of measured cumulative amounts of electric energy is to be retrieved 2"
    }

    def __init__(self, host, api_connector, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x88
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
