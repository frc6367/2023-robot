#!/usr/bin/env python3
"""
    This is a demo program showing how to use Mecanum control with the
    MecanumDrive class.
"""

import ctre
import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):
    # Channels on the roboRIO that the motor controllers are plugged in to
    kFrontLeftChannel = 2
    kRearLeftChannel = 3
    kFrontRightChannel = 6
    kRearRightChannel = 5

    # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1

    def robotInit(self):
        self.frontLeft = ctre.WPI_VictorSPX(self.kFrontLeftChannel)
        self.rearLeft = ctre.WPI_VictorSPX(self.kRearLeftChannel)
        self.frontRight = ctre.WPI_VictorSPX(self.kFrontRightChannel)
        self.rearRight = ctre.WPI_VictorSPX(self.kRearRightChannel)

        # invert the right side motors
        # you may need to change or remove this to match your robot
        self.frontRight.setInverted(True)
        self.rearRight.setInverted(True)

        self.robotDrive = wpilib.drive.MecanumDrive(
            self.frontLeft, self.rearLeft, self.frontRight, self.rearRight
        )

        self.stick0 = wpilib.Joystick(self.kJoystickChannel0)
        self.stick1 = wpilib.Joystick(self.kJoystickChannel1)

    def teleopPeriodic(self):
        # Use the joystick X axis for lateral movement, Y axis for forward
        # movement, and Z axis for rotation.
        self.robotDrive.driveCartesian(
            -self.stick0.getY(),
            self.stick0.getX(),
            self.stick1.getZ(),
        )


if __name__ == "__main__":
    wpilib.run(MyRobot)
