import magicbot
import wpilib.drive
import rev

class Grabber:
    intake: rev.CANSparkMax(6, rev.CANSparkMax.MotorType.kBrushless)
    intake: rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)

    #
    # Action methods
    #

    def grab(self):
        pass
    def release(self):
        pass

    #
    #Feedback mathods
    #
    @magicbot.feedback
    def hasObject(self):
        pass
    @magicbot.feedback
    def isOpen(self):
        pass
    @magicbot.feedback
    def isClosed(self):
        pass
    @magicbot.feedback
    def isObjectSensed(self):
        pass

    #
    #Execute
    #
    
    def execute(self):
        pass