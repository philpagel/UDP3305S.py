"Power supply channel"

class channel:
    """PSU channel
    Implementaton of all channel features.
    """

    def __init__(self, name, connection, V_max, A_max, write, query):
        """Initialize channel object

    name        name of the channel
    connection  connection object to read/write from/to
    V_max       max voltage supported
    A_max       max current supported
"""

        self.connection = connection
        self.name = name
        self.V_max = V_max
        self.A_max = A_max
        self.write = write
        self.query = query


    @property
    def voltage(self):
        "output voltage [V]"
        return float(self.query(f"APPLY? {self.name},VOLT").split(",")[1])

    @voltage.setter
    def voltage(self, value):
        if 0 <= value <= self.V_max:
            self.write(f"APPLY {self.name},{value}V")
        else:
            raise ValueError(f"Voltage must be in [0, {self.V_max}V")
    
    @property
    def current(self):
        "output current limit [A]"
        return (
            float(self.query(f"APPLY? {self.name},CURRENT").split(",")[1])
        )

    @current.setter
    def current(self, value):
        if 0 <= value <= self.A_max:
            self.write(f"APPLY {self.name},{value}A")
        else:
            raise ValueError(f"Current must be in [0, {self.A_max}V")
    
    @property
    def OVP(self):
        "over voltage protection (OVP) value [V]"
        value = float(self.query(f"OUTPUT:OVP:VALUE? {self.name}"))
        state = self.query(f"OUTPUT:OVP:STATE? {self.name}")
        return (value, state)

    @OVP.setter
    def OVP(self, value, state=1):
        if 0 <= value <= self.V_max:
            self.write(f"OUTPUT:OVP:VALUE {self.name},{value}")
        else:
            raise ValueError(f"OVP Voltage must be in [0, {self.V_max}V")

        if state.upper() in ("ON", "OFF", 1, 0):
            self.write(f"OUTPUT:OVP:STATE {self.name},{state}")
        else:
            raise ValueError(f"'{state}' is not a valid OVP state.")

    @property
    def OCP(self):
        "over current protection (OCP) value [A]"
        value = float(self.query(f"OUTPUT:OCP:VALUE? {self.name}"))
        state = self.query(f"OUTPUT:OCP:STATE? {self.name}")
        return (value, state)
    
    @OCP.setter
    def OCP(self, value, state=1):
        if 0 <= value <= self.A_max:
            self.write(f"OUTPUT:OCP:VALUE {self.name},{value}")
        else:
            raise ValueError(f"OCP current must be in [0, {self.A_max}A")

        if state.upper() in ("ON", "OFF", 1, 0):
            self.write(f"OUTPUT:OCP:STATE {self.name},{state}")
        else:
            raise ValueError(f"'{state}' is not a valid OCP state.")

    def read_voltage(self):
        "read (measure) output voltage [V]"

        return float(self.query(f"MEASURE:VOLT? {self.name}"))

    def read_current(self):
        "read (measure) output current [A]"

        return float(self.query(f"MEASURE:CURRENT? {self.name}"))

    def read_power(self):
        "read (measure) output power [W]"

        return float(self.query(f"MEASURE:POWER? {self.name}"))

    def read_all(self):
        "read (measure) output values: Volts [V], current [A], Power[W]"

        ret = [float(x) for x in self.query(f"MEASURE:ALL? {self.name}").split(",")]
        return ret

    @property
    def output(self):
        "channel output state"
        return self.query(f"OUTPUT:STATE? {self.name}")

    @output.setter
    def output(self, value):
        if value.upper() in ("ON", "OFF"):
            self.write(f"OUTPUT:STATE {self.name},{value}")
        else:
            raise ValueError (f"Invalid output state '{value}'")

    def on(self):
        "turn output on"
        self.write(f"OUTPUT:STATE {self.name},ON")

    def off(self):
        "turn output off"
        self.write(f"OUTPUT:STATE {self.name},OFF")

