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



    #
    #Execute
    #