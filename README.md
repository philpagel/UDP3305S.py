# UPD3305S

Python class for controlling Uni-T UDP3305S or UDP3305S-E lab power supply units.

# In a nutshell

    #!/bin/env python3
    import time, datetime
    from UDP3305S import UDP3305S

    psu = UDP3305S("TCPIP::192.168.0.66::INSTR")

    # setup voltage and current limits
    psu.ch1.voltage(13.5)
    psu.ch1.current(3)
    psu.ch2.voltage(24)
    psu.ch2.current(4.5)

    # activate the first two channels
    psu.ch1.on()
    psu.ch2.on()

    # log current and power for about 30 seconds
    print("timestamp, A1, P1, A2, P2")
    for i in range(30):
        print(", ".join([str(x) for x in [
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                psu.ch1.read_current(),
                psu.ch1.read_power(),
                psu.ch1.read_current(),
                psu.ch1.read_power(),
        ]]))
        time.sleep(1)

    # turn off all channels
    psu.off()


# Status

[![works on my machine badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.4.0/badge.svg)](https://github.com/nikku/works-on-my-machine)
UDP3305S, LINUX.

| Feature                    | Status |
|--------------------------- |------- |
| Output on/off              | ✓      |
| All 3 channels             | ✓      |
| Set/get voltage, current   | ✓      |
| OCP, OVP                   | ✓      |
| Voltage, current readout   | ✓      |
| List mode                  | —      |
| Delayer mode               | —      |

# Reference

XXX: to be written

# Contributing

If you think you found a bug or you have an idea for a new feature, please open
an issue here on GitHub. Please **do not submit pull-requests before discussing
the issue** you want to address.

If you want to report a bug, please make sure to replicate the erroneous
behavior at least once before opening an issue and provide all information
necessary to replicate the problem (what commands did you use, what was
connected to the load, what did you observe, what did you expect?).

I would very much appreciate help from people who own any of the various models
listed above: It would be great if they could run the automated tests on their
devices and let me know if that went fine or produced errors. Please get in
touch if you would like to do that. Also any feedback and bug reports are
welcome.

