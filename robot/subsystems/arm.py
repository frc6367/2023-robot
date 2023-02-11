import magicbot
import wpilib.drive
import rev

class Arm:
    intake: rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)

    #
    # Action methods
    #

    def gotoHi(self):
        pass
    def gotoMiddle(self):
        pass
    def gotoLow(self):
        pass
    def gotoNetural(self):
        pass
    
    #
    #Feedback mathods
    #

    @magicbot.feedback
    def getAngle(self):
        pass
    @magicbot.feedback
    def getPosition(self):
        pass

    #
    #Execute
    #

    def execute(self):
        pass