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

    def __init__(self,
        RID,
        baudrate=9600,
        eol_r="\n",
        eol_w="\n",
        delay=0.2,
        timeout=2000,
        model=None,
        ):
        """Initialize PSU instance

RID (Resource ID) as defined by pyVISA. E.g.:

    TCPIP::192.168.0.66::INSTR
    TCPIP::PowerSupply::INSTR
    GPIB1::10
    USB::0x1234::125::A22-5::INSTR

    See pyVISA documentation for details.
"""
        rm = pyvisa.ResourceManager()
        
        self.connection = None
        i = 0
        while i < 3 and self.connection is None:    # up to 3 connection trys
            try:
                self.connection = rm.open_resource(RID)
            except pyvisa.errors.VisaIOError:
                i += 1
                time.sleep(0.2)
            if self.connection is not None:
                break
        if self.connection is None:
            exit("Could not connect to device.")

        self.connection.baud_rate = baudrate
        self.connection.query_delay = delay
        self.connection.timeout = timeout
        self.connection.read_termination = eol_r
        self.connection.write_termination = eol_w

        self.idn = dict()
        (self.idn['manufacturer'], 
         self.idn['model'], 
         self.idn['SN'], 
         self.idn['firmware']) = self.connection.query("*IDN?").split(",")
        
        if self.idn["model"] not in ("UDP3305S", "UDP3305S-E"):
            raise RuntimeError(f"Instrument ID '{self.idn['model']}' not supported." )

        self.ch1 = channel("CH1", self.connection, V_max=33, A_max=5.2,  write=self.write, query=self.query)
        self.ch2 = channel("CH2", self.connection, V_max=33, A_max=5.2, write=self.write, query=self.query)
        self.ch3 = channel("CH3", self.connection, V_max=6.2, A_max=3.2, write=self.write, query=self.query)
        self.chSER = channel("SER", self.connection, V_max=66, A_max=5.2, write=self.write, query=self.query)
        self.chPAR = channel("PARA", self.connection, V_max=33, A_max=10.4, write=self.write, query=self.query)

        self.Channels = (self.ch1, self.ch2, self.ch3, self.chSER, self.chPAR)

    def __del__(self):
        self.connection.close()

    def __str__(self):
        return f"{self.idn['model']} 3-channel lab power supply\nSN:{self.idn['SN']}\nFirmware: {self.idn['firmware']}"

    def write(self, command):
        "write command to connection"
        self.connection.write(command)
        time.sleep(self.connection.query_delay)

    def query(self, command, nrows=1, timeout=None):
        """Write command to connection and return answer value
        By default, reads 1 line of response.
        If you expect more, you need to set `nrows` to the respective value
        If you expect the respinse to be slow, you can set a ne timout just for
        this request
        """

        if timeout is not None:
            _timeout = self.connection.timeout
            self.connection.timeout = timeout
        
        self.connection.write(command)
        time.sleep(self.connection.query_delay)
        ret = []
        for i in range(nrows):
            value = self.connection.read()
            time.sleep(self.connection.query_delay)
            ret.append(value)
        if timeout is not None:
            self.connection.timeout = _timeout
        return ret if len(ret) > 1 else ret[0]

    @property
    def mode(self):
        "output mode (NORMAL | SER | PARA)"
        return self.connection.query("SOURCE:MODE?")

    @mode.setter
    def mode(self, mode):
        if mode.upper() in ("NORMAL", "NORM", "SER", "PARA"):
            self.write(f"SOURCE:MODE {mode}")
            time.sleep(0.5)
        else:
            raise ValueError(f"'{mode}' is not a valid output mode")

    def reset(self):
        "reset the device"
        self.write(f"RST")

    def on(self):
        "turn on all outputs"
        self.write(f"OUTPUT:STATE ALL,ON")

    def off(self):
        "turn off all outputs"
        self.write(f"OUTPUT:STATE ALL,OFF")

    def lock(self):
        "lock keys on instrument panel"
        self.write("LOCK ON")
    
    def unlock(self):
        "unlock keys on instrument panel"
        self.write("LOCK OFF")


