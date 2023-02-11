import magicbot
import wpilib.drive
import rev


class Arm:
    arm_motor: rev.CANSparkMax

    HI_MIN = 6
    HI_MAX = 7

    MID_MIN = 4
    MID_MAX = 5

    LOW_MIN = 2
    LOW_MAX = 3

    NETURAL_MIN = 0
    NETURAL_MAX = 1

    #
    # Action methods
    #

    def gotoHi(self):
        self.gotoAngle = 20

    def gotoMiddle(self):
        self.gotoAngle = 15

    def gotoLow(self):
        self.gotoAngle = 10

    def gotoNetural(self):
        self.gotoAngle = 5

    #
    # Feedback mathods
    #

    @magicbot.feedback
    def getAngle(self):
        encoder = self.arm_motor.getEncoder()

    @magicbot.feedback
    def getPosition(self):
        encoder = self.arm_motor.getEncoder()
        p = encoder.getPosition()
        if p > self.LOW_MIN and p < self.LOW_MAX:
            return "LOW"
        if p > self.MID_MIN and p < self.MID_MAX:
            return "MID"
        if p > self.HI_MIN and p < self.HI_MAX:
            return "HI"
        if p > self.NETURAL_MIN and p < self.NETURAL_MAX:
            return "NETURAL"
        return ""

    #
    # Execute
    #

    def execute(self):
        pass