import wpilib
import magicbot

import ctre
import rev
import navx

class MyRobot(magicbot.MagicRobot):

    def createObjects(self):
        self.joystick = Joystick(0)
        self. joystick2 = Joystick(1)

        self.frontLeftMotor = ctre.WPI_TalonSRX(4)
        self.rearLeftMotor = ctre.WPI_TalonSRX(3)
        self.frontRightMotor = ctre.WPI_TalonSRX(1)
        self.rearRightMotor = ctre.WPI_TalonSRX(2)

        self.frontRightMotor.setInverted(True)
        self.rearRightMotor.setInverted(True)
    
        self.arm_motor = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        self.grabber_motor = rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)

    def teleopInit(self):
        pass
    
    def teleopPeriodic(self):
        pass

if __name__ == '__main__':
    wpilib.run(MyRobot)

