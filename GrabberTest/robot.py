#!/usr/bin/env python3
"""
    This is a demo program showing the use of the RobotDrive class,
    specifically it contains the code necessary to operate a robot with
    tank drive.
"""

import rev
import wpilib


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """Robot initialization function"""

        self.grabber = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        self.encoder = self.grabber.getEncoder()

        self.arm1 = rev.CANSparkMax(6, rev.CANSparkMax.MotorType.kBrushless)
        self.arm2 = rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)

        self.arm_encoder = self.arm1.getEncoder()

        self.arm2.follow(self.arm1, True)

        # joysticks 1 & 2 on the driver station
        self.stick = wpilib.Joystick(0)

    def teleopInit(self) -> None:
        print("In teleopInit")

    def teleopPeriodic(self):
        wpilib.SmartDashboard.putNumber("curent", self.grabber.getOutputCurrent())
        wpilib.SmartDashboard.putNumber("speed", self.stick.getRawAxis(3))
        wpilib.SmartDashboard.putNumber("Grabber-encoder", self.encoder.getPosition())
        wpilib.SmartDashboard.putNumber("Arm1-encoder", self.arm_encoder.getPosition())

        if self.stick.getRawButton(11):
            self.grabber.set(self.stick.getRawAxis(3))
        elif self.stick.getRawButton(12):
            self.grabber.set(-self.stick.getRawAxis(3))
        else:
            self.grabber.set(0)

        if self.stick.getTrigger():
            self.arm1.set(self.stick.getY())
        else:
            self.arm1.set(0)


if __name__ == "__main__":
    wpilib.run(MyRobot)
