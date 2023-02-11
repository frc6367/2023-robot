import magicbot
import wpilib.drive
import rev

class Arm:
    intake: rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)

    def hi(self):
        pass
    def middle(self):
        pass
    def low(self):
        pass
    def netural(self):
        pass
    
    wpilib.SmartDashboard.