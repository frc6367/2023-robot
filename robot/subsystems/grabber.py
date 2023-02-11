import magicbot
import wpilib.drive
import rev

class Grabber:
    intake: rev.CANSparkMax(6, rev.CANSparkMax.MotorType.kBrushless)
    intake: rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)

    def grab(self):
        pass
    def release(self):
        pass

    