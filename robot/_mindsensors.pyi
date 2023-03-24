from __future__ import annotations
import typing
import wpilib._wpilib

__all__ = [
    "CANLight"
]


class CANLight():
    def __init__(self, deviceNumber: int) -> None: 
        """
        An instance of this object represents a single CANLight device. Multiple
        devices can be used indepentently to control multiple light strips. Only a
        single instance can be created for each device ID. Please construct this
        object only once when initializing your robot and pass the reference around.
        If you do wish to call this constructor with the same ID later, call the
        destructor first.

        If a CANLight does not have a CAN connection to a roboRIO, its default
        behavior of :meth:`.Cycle` will be used. If it
        does find a CAN connection, it will execute {@link #ShowRegister(int)
        ShowRegister(0)}. The CANLight will continue to execute its last command
        until a new one is issued via one of the methods detailed below.

        The CANLight can hold a sequence of up to eight colors and associated
        durations. Each register has a default value. The WriteRegister command can
        be used to change these. The CANLight will restore its default values when
        power is lost.

        :param deviceNumber: An integer between 1 and 60 (inclusive) for the ID of
                             this CANLight. CAN IDs can be modified through the mindsensors
                             configuration tool, available at
                             <a href="http://www.mindsensors.com/pages/311">mindsensors.com/pages/311
                             </a>. Devices will ship with a factory default CAN ID of 3. Please use a
                             unique ID for each device.
        """
    def blinkLED(self, seconds: int) -> None: 
        """
        Each CANLight has a build-in LED on the board itself. This command will cause
        it to blink for a specified duration. This can be useful in debugging. Please
        do not confuse this with a fast flashing pattern, which signifies that the
        CANLight can not find a connection to the FRC driver station.

        :param seconds: The number of seconds to blink.
        """
    def cycle(self, fromIndex: int, toIndex: int) -> None: 
        """
        Cycle through a sequence of stored color values.

        :param fromIndex: An integer between 0 and 7 (inclusive) for which register to
                          begin the sequence at.
        :param toIndex:   An integer between 0 and 7 (inclusive) for which register to
                          use as the last color in the sequence.
        """
    def fade(self, startIndex: int, endIndex: int) -> None: 
        """
        Fade across a sequence of stored color values. Similar to
        :meth:`.Cycle`, but fading between colors instead of
        jumping to them. The duration value of each register specifies how long it
        will take to fade from that color.

        :param startIndex: An integer between 0 and 7 (inclusive) for which register
                           to begin at.
        :param endIndex:   An integer between 0 and 7 (inclusive) for which register to
                           end at.
        """
    def flash(self, index: int) -> None: 
        """
        Flash a stored color. Lights will remain on and off for the time specified in
        this register.

        :param index: An integer between 0 and 7 (inclusive) for which register to
                      show.
        """
    def getBatteryVoltage(self) -> float: 
        """
        :returns: The voltage this CANLight device is currently receiving. A value of
                  0.0 likely indicates this CANLight is not connected properly. Please check
                  the CAN and power connections, or look to the CANLight user guide on
                  mindsensors.com.
        """
    def getBootloaderVersion(self) -> str: 
        """
        :returns: The bootloader version of this CANLight. The bootloader is used to
                  update firmware on the CANLight.
        """
    def getDeviceID(self) -> int: 
        """
        :returns: The device ID provided when constructing this CANLight instance.
        """
    def getDeviceName(self) -> str: 
        """
        :returns: The name associated with this CANLight. The factory default will be
                  "CANLight", but this value can be changed through the mindsensors
                  configuration tool.
        """
    def getFirmwareVersion(self) -> str: 
        """
        :returns: The firmware version of this CANLight. Firmware can be updated
                  through the mindsensors configuration tool. This may be considered during
                  inspection at competitions. Firmware updates can provide new features. The
                  firmware version of the CANLight device must be compatible with this library.
        """
    def getHardwareVersion(self) -> str: 
        """
        :returns: The hardware version of this CANLight. Any hardware revisions will
                  have a different hardware version number.
        """
    @staticmethod
    def getLibraryVersion() -> str: ...
    def getSerialNumber(self) -> str: 
        """
        :returns: The serial number of this device. Each serial number is unique and
                  may be requested for customer support.
        """
    def reset(self) -> None: 
        """
        Restore the registers to power on default. These are, in order, from index
        0 to 7: off, red, green, blue, orange, teal, purple, white.
        """
    @typing.overload
    def showRGB(self, color: wpilib._wpilib.Color8Bit) -> None: 
        """
        Set a static color for the CANLight to display. This command will simply set
        red, green, and blue values for the RGB LED strip. The CANLight will continue
        to display this color until a new command is called.

        :param red:   An integer between 0 and 255 (inclusive) for the red component of
                      the color to show.
        :param green: An integer between 0 and 255 (inclusive) for the green component
                      of the color to show.
        :param blue:  An integer between 0 and 255 (inclusive) for the blue component
                      of the color to show.
        """
    @typing.overload
    def showRGB(self, red: int, green: int, blue: int) -> None: ...
    def showRegister(self, index: int) -> None: 
        """
        Display a stored color. As with :meth:`.ShowRGB`
        this color will be displayed until a new command is issued.

        :param index: An integer between 0 and 7 (inclusive) for which register to
                      show.
        """
    @typing.overload
    def writeRegister(self, index: int, time: float, color: wpilib._wpilib.Color8Bit) -> None: 
        """
        Write a value in the CANLight's internal memory. The CANLight has 8 internal
        memory slots (registers) for use in commands like
        :meth:`.Cycle`. The time value will determine how long a
        color will display with :meth:`.Flash` or
        :meth:`.Cycle`, or how long it will take to
        :meth:`.Fade` from this color. They have preset values, but
        this command allows for changing the stored colors. The registers will return
        to their default values when the CANLight loses power. A robot's
        initialization function can be a good place to set up these values.

        :param index: An integer between 0 and 7 (inclusive) for which register to
                      write to.
        :param time:  The duration, in seconds, to use in commands like
                      :meth:`.Flash` or :meth:`.Cycle`. Value less than
                      1 can be used, such as 0.25 for a quarter of a second.
        :param red:   An integer between 0 and 255 (inclusive).
        :param green: An integer between 0 and 255 (inclusive).
        :param blue:  An integer between 0 and 255 (inclusive).
        """
    @typing.overload
    def writeRegister(self, index: int, time: float, red: int, green: int, blue: int) -> None: ...
    pass
