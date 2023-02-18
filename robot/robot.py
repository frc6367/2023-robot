import wpilib
import magicbot

import ctre
import rev
import navx
from subsystems.grabber import Grabber
from subsystems.drivetrain import DriveTrain


class MyRobot(magicbot.MagicRobot):
    grabber: Grabber
    drivetrain: DriveTrain

    def createObjects(self):
        self.joystick = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        self.drive_l1 = ctre.WPI_TalonSRX(4)
        self.drive_l2 = ctre.WPI_TalonSRX(3)
        self.drive_r1 = ctre.WPI_TalonSRX(1)
        self.drive_r2 = ctre.WPI_TalonSRX(2)

        self.drive_r1.setInverted(True)
        self.drive_r2.setInverted(True)

        self.arm_motor = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        self.grabber_motor = rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)
        self.grabber_motor.setInverted(True)

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        if self.joystick.getRawButton(3):
            self.grabber.grab()
        elif self.joystick.getRawButton(4):
            self.grabber.release()
        else:
            self.grabber.stop()
        if self.joystick.getY():
            


if __name__ == "__main__":
    wpilib.run(MyRobot)
