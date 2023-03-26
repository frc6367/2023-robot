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
PINK = wpilib.Color8Bit(wpilib.Color.kPink)
ORANGE = wpilib.Color8Bit(wpilib.Color.kOrange)
YELLOW = wpilib.Color8Bit(wpilib.Color.kYellow)
YELLOWGREEN = wpilib.Color8Bit(wpilib.Color.kYellowGreen)

ELECTROLIGHTS_BLUE = wpilib.Color8Bit(0x0D, 0xA1, 0xE6)
ELECTROLIGHTS_PURPLE = wpilib.Color8Bit(wpilib.Color.kPurple)


class LEDController:
    color = magicbot.will_reset_to(ELECTROLIGHTS_PURPLE)

    def __init__(self) -> None:
        if CANLight:
            print("LED present")
            self.light = CANLight(3)

            # register colors with the controller that we can reference by index
            self.light.writeRegister(0, 2, ELECTROLIGHTS_BLUE)
            self.light.writeRegister(1, 2, ELECTROLIGHTS_PURPLE)
            self.light.writeRegister(2, 2, RED)

        else:
            print("LED not present")
            self.light = None

    def disabledPeriodic(self):
        if not self.light:
            return

        alliance = wpilib.DriverStation.getAlliance()
        if alliance == wpilib.DriverStation.Alliance.kBlue:
            self.light.fade(0, 1)
        elif alliance == wpilib.DriverStation.Alliance.kRed:
            self.light.fade(1, 2)
        else:
            # fade between electrolights blue/purple
            self.light.fade(0, 1)

    def indicateHasCube(self):
        self.color = GREEN

    def indicateMaybeCube(self):
        self.color = YELLOW

    def indicateAlmostCube(self):
        self.color = YELLOWGREEN

    def indicateArmUp(self):
        self.color = RED

    # TODO: add robot autobalance indicators

    def execute(self):
        if not self.light:
            return

        self.light.showRGB(self.color)
