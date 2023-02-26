#!/usr/bin/env python3

import wpilib
import magicbot

from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A41

import ctre
import rev
import navx

import constants
from misc.ejoystick import EnhancedJoystick
from subsystems.grabber import Grabber
from subsystems.drivetrain import DriveTrain
from subsystems.arm import Arm
from components.auto_grabber import AutoGrabber


class MyRobot(magicbot.MagicRobot):
    auto_grab: AutoGrabber
    grabber: Grabber
    drivetrain: DriveTrain
    arm: Arm

    def createObjects(self):
        # Joysticks
        self.stick = EnhancedJoystick(0)

        # Drivetrain
        self.drive_l1 = ctre.WPI_TalonSRX(4)
        self.drive_l2 = ctre.WPI_TalonSRX(3)
        self.drive_r1 = ctre.WPI_TalonSRX(1)
        self.drive_r2 = ctre.WPI_TalonSRX(2)

        self.drive_r1.setInverted(True)
        self.drive_r2.setInverted(True)

        self.encoder_l = wpilib.Encoder(0, 1)
        self.encoder_r = wpilib.Encoder(2, 3)
        self.encoder_l.setDistancePerPulse(constants.kDistancePerPulse)
        self.encoder_r.setDistancePerPulse(constants.kDistancePerPulse)
        self.encoder_r.setReverseDirection(True)

        # Gyro
        self.ahrs = navx.AHRS.create_spi()

        # Arm
        self.arm_motor = rev.CANSparkMax(6, rev.CANSparkMax.MotorType.kBrushless)
        self.arm_motor2 = rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)

        # Grabber
        self.grabber_motor = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        self.grabber_sensor = SharpIR2Y0A41(0)

    @magicbot.feedback
    def left_encoder(self) -> int:
        return self.encoder_l.get()

    @magicbot.feedback
    def right_encoder(self) -> int:
        return self.encoder_r.get()

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        # drivetrain logic goes first
        speed = -self.stick.getEnhY()
        rotation = -self.stick.getEnhTwist()

        self.drivetrain.move(speed, rotation)

        if self.stick.getRawButton(7):
            self.arm.gotoHi()
        elif self.stick.getRawButton(9):
            self.arm.gotoMiddle()
        elif self.stick.getRawButton(11):
            self.arm.gotoLow()
        elif self.stick.getRawButton(12):
            self.arm.gotoNeutral()

        if self.stick.getRawButton(1):
            self.grabber.grab()
        elif self.stick.getRawButton(2):
            self.grabber.release()
        else:
            self.auto_grab.activate()


if __name__ == "__main__":
    wpilib.run(MyRobot)
