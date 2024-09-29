"power supply nase instrument"

import sys, time, pyvisa
from .channel import channel

class UDP3305S:
    """Uni-T UDP3305S Lab power supply

    Features 5 channels:
    
        ch1     channel1
        ch2     channel2
        ch3     channel3
        chSER   virtual channel vor serial mode
        chPAR   virtual channel for parallel mode
"""

    def __init__(self, RID):
        """Initialize PSU instance

RID (Resource ID) as defined by pyVISA. E.g.:

    TCPIP::192.168.0.66::INSTR
    TCPIP::PowerSupply::INSTR
    GPIB1::10
    USB::0x1234::125::A22-5::INSTR

    See pyVISA documentation for details.
"""
        rm = pyvisa.ResourceManager()
        self.connection = rm.open_resource(RID)
        self.connection.read_termination = "\n"
        self.connection.write_termination = "\n"
        self.idn = dict()
        (self.idn['manufacturer'], 
         self.idn['model'], 
         self.idn['SN'], 
         self.idn['firmware']) = self.connection.query("*IDN?").split(",")
        
        if self.idn["model"] not in ("UDP3305S", "UDP3305S-E"):
            raise RuntimeError(f"Instrument ID '{self.idn['model']}' not supported." )

        self.ch1 = channel("CH1", self.connection, V_max=33, A_max=5.2)
        self.ch2 = channel("CH2", self.connection, V_max=33, A_max=5.2)
        self.ch3 = channel("CH3", self.connection, V_max=6.2, A_max=3.2)
        self.chSER = channel("SER", self.connection, V_max=66, A_max=5.2)
        self.chPAR = channel("PAR", self.connection, V_max=33, A_max=10.4)

    def __del__(self):
        self.connection.close()

    def __str__(self):
        return f"{self.idn['model']} 3-channel lab power supply\nSN:{self.idn['SN']}\nFirmware: {self.idn['firmware']}"

    def get_mode(self):
        "return output mode (NORMAL | SER | PARA)"
        return self.connection.query("SOURCE:MODE?")

    def set_mode(self, mode):
        "set output mode (NORMAL | SER | PARA)"

        if mode.upper() in ("NORMAL", "NORM", "SER", "PARA"):
            self.connection.write(f"SOURCE:MODE {mode}")
        else:
            raise ValueError(f"'{mode}' is not a valid output mode")

    def on(self):
        "turn on all outputs"
        self.connection.write(f"OUTPUT:STATE ALL,ON")

    def off(self):
        "turn off all outputs"
        self.connection.write(f"OUTPUT:STATE ALL,OFF")

    def lock(self):
        "lock keys on instrument panel"
        self.connection.write("LOCK ON")
    
    def unlock(self):
        "unlock keys on instrument panel"
        self.connection.write("LOCK OFF")


