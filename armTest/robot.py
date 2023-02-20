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

        # joysticks 1 & 2 on the driver station
        self.stick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        wpilib.SmartDashboard.putNumber("curent", self.grabber.getOutputCurrent())
        wpilib.SmartDashboard.putNumber("speed", self.stick.getZ())
        wpilib.SmartDashboard.putNumber(
            "encoder", self.grabber.getEncoder().getPosition()
        )

        if self.stick.getRawButton(11):
            self.grabber.set(self.stick.getZ())
        else:
            self.grabber.set(0)


if __name__ == "__main__":
    wpilib.run(MyRobot)
