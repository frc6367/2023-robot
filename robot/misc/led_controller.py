import magicbot
import wpilib

try:
    from _mindsensors import CANLight
except ImportError:
    CANLight = None

# Various colors

RED = wpilib.Color8Bit(wpilib.Color.kRed)
BLUE = wpilib.Color8Bit(wpilib.Color.kBlue)
GREEN = wpilib.Color8Bit(wpilib.Color.kGreen)
YELLOW = wpilib.Color8Bit(wpilib.Color.kYellow)
YELLOWGREEN = wpilib.Color8Bit(wpilib.Color.kYellowGreen)

ELECTROLIGHTS_BLUE = wpilib.Color8Bit(0x0D, 0xA1, 0xE6)
ELECTROLIGHTS_PURPLE = wpilib.Color8Bit(wpilib.Color.kPurple)


class LEDController:

    color = magicbot.will_reset_to(ELECTROLIGHTS_PURPLE)

    def __init__(self) -> None:
        if CANLight:
            self.light = CANLight(3)

            # register colors with the controller that we can reference by index
            self.light.writeRegister(0, 2, ELECTROLIGHTS_BLUE)
            self.light.writeRegister(1, 2, ELECTROLIGHTS_PURPLE)

        else:
            self.light = None

    def disabledPeriodic(self):
        if not self.light:
            return

        alliance = wpilib.DriverStation.getAlliance()
        if alliance == wpilib.DriverStation.Alliance.kBlue:
            self.light.showRGB(BLUE)
        elif alliance == wpilib.DriverStation.Alliance.kRed:
            self.light.showRGB(RED)
        else:
            # fade between electrolights blue/purple
            self.light.fade(0, 1)

    def indicateHasCube(self):
        self.color = GREEN

    def indicateMaybeCube(self):
        self.color = YELLOW

    def indicateAlmostCube(self):
        self.color = YELLOWGREEN

    # TODO: add robot autobalance indicators

    def execute(self):
        if not self.light:
            return

        self.light.showRGB(self.color)
