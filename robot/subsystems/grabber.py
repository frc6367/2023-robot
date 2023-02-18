import magicbot
import wpilib.drive
import rev


class Grabber:
    grabber_motor: rev.CANSparkMax

    #
    # Action methods
    #

    def grab(self):
        pass
    
        

    def release(self):
        pass

    #
    # Feedback mathods
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
    # Execute
    #

    def execute(self):
        pass
