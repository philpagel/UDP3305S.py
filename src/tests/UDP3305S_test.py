import pytest
from time import sleep
from UDP3305S import UDP3305S
from .testconfig import *

psu = UDP3305S(RID)
psu.reset()
sleep(5)
psu.mode="Normal"
psu.off()

print("\nModel: ", psu.idn["model"])
print("Firmware: ", psu.idn["firmware"])

def test_output_state():
    "setting and getting channel on/off state"

    psu.mode = "normal"
    psu.on()
    assert psu.ch1.output == "ON"
    assert psu.ch2.output == "ON"
    assert psu.ch3.output == "ON"
    
    psu.off()
    assert psu.ch1.output == "OFF"
    assert psu.ch2.output == "OFF"
    assert psu.ch3.output == "OFF"

    psu.ch1.output = "on"
    assert psu.ch1.output == "ON"
    assert psu.ch2.output == "OFF"
    assert psu.ch3.output == "OFF"

    psu.ch2.output = "on"
    assert psu.ch1.output == "ON"
    assert psu.ch2.output == "ON"
    assert psu.ch3.output == "OFF"

    psu.ch1.output = "off"
    psu.ch3.output = "on"
    assert psu.ch1.output == "OFF"
    assert psu.ch2.output == "ON"
    assert psu.ch3.output == "ON"
    
    psu.off()
    psu.mode = "SER"
    psu.chSER.output = "OFF"
    psu.chSER.output = "ON"
    assert psu.chSER.output == "ON"

    psu.off()
    psu.mode = "PARA"
    assert psu.chPAR.output == "OFF"
    psu.chPAR.output = "ON"
    assert psu.chPAR.output == "ON"


def test_channel_pars():

    psu.off()
    psu.mode = "normal"
    for ch in psu.Channels[:3]:
        if ch.name == "SER":
            psu.mode = "SER"
        elif ch.name == "PARA":
            psu.mode = "PARA"

        ch.voltage = 0
        assert ch.voltage == 0
        ch.voltage = 5.125
        assert ch.voltage == 5.125

        ch.current = 0.000
        assert ch.current == 0
        ch.current = 0.543
        assert ch.current == 0.543



def test_measure():
    """measuring voltage, current and power
    """

    psu.off()
    psu.mode = "normal"
    for ch in psu.Channels:
        if ch.name == "SER":
            psu.mode = "SER"
        elif ch.name == "PARA":
            psu.mode = "PARA"

        ch.voltage = 5.5
        ch.current = 2
        ch.on()
        sleep(0.5)
        assert abs(ch.read_voltage() - 5.5) < 0.01
        assert ch.read_current() <= 0.01
        assert ch.read_power() <= 0.01
        
        ch.voltage = 3.5
        sleep(0.5)
        assert abs(ch.read_voltage() - 3.5) < 0.01
        assert ch.read_current() <= 0.01
        assert ch.read_power() <= 0.01

        ch.off()
    

