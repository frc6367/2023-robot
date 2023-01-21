#!/usr/bin/env python3
"""
    This is a demo program showing the use of the RobotDrive class,
    specifically it contains the code necessary to operate a robot with
    tank drive.
"""

import ctre
import navx
import wpilib
from wpilib.drive import DifferentialDrive


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """Robot initialization function"""

        # object that handles basic drive operations
        self.frontLeftMotor = ctre.WPI_TalonSRX(4)
        self.rearLeftMotor = ctre.WPI_TalonSRX(3)
        self.frontRightMotor = ctre.WPI_TalonSRX(1)
        self.rearRightMotor = ctre.WPI_TalonSRX(2)

        # Timer for autonomys
        self.timer = wpilib.Timer()

        self.gyro = navx.AHRS.create_spi()

        # invert the right side motors
        # you may need to change or remove this to match your robot
        self.frontRightMotor.setInverted(True)
        self.rearRightMotor.setInverted(True)

        self.left = wpilib.MotorControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.MotorControllerGroup(
            self.frontRightMotor, self.rearRightMotor
        )

        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        # joysticks 1 & 2 on the driver station
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)

    def teleopInit(self):
        """Executed at the start of teleop mode"""
        self.myRobot.setSafetyEnabled(True)

    def teleopPeriodic(self):
        """Runs the motors with tank steering"""
        self.myRobot.tankDrive(self.leftStick.getY() * -1, self.rightStick.getY() * -1)

    # Autonomous
    def autonomousInit(self) -> None:
        self.timer.reset()
        self.timer.start()
        self.gyro.reset()

    def autonomousPeriodic(self) -> None:
        if self.timer.get() < 3.0:
            self.myRobot.arcadeDrive(0.25, 0, False)
        elif self.timer.get() < 5.0:
            self.myRobot.arcadeDrive(0, 0, False)
        elif self.timer.get() < 10.0:
            a = self.gyro.getAngle()
            v = 0.8 + (a / 180) * 0.8
            self.myRobot.arcadeDrive(0, v, False)
        elif self.timer.get() < 13.0:
            self.myRobot.arcadeDrive(0.25, 0, False)
        elif self.timer.get() < 15.0:
            self.myRobot.arcadeDrive(0, 0, False)
            self.gyro.reset()
        elif self.timer.get() < 20.0:
            a = self.gyro.getAngle()
            v = 0.8 + (a / 180) * 0.8
            self.myRobot.arcadeDrive(0, v, False)
        elif self.timer.get() < 23.0:
            self.myRobot.arcadeDrive(0.25, 0, False)
        else:
            self.myRobot.arcadeDrive(0, 0, False)


if __name__ == "__main__":
    wpilib.run(MyRobot)
