#!/usr/bin/env python3

import wpilib
import magicbot

from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A41

import ctre
import navx
import rev

import constants

from misc.ejoystick import EnhancedJoystick
from misc.sparksim import CANSparkMax

from subsystems.grabber import Grabber
from subsystems.drivetrain import DriveTrain
from subsystems.arm import Arm

from components.auto_grabber import AutoGrabber
from components.auto_balance import AutoBalance


class MyRobot(magicbot.MagicRobot):
    auto_grab: AutoGrabber
    grabber: Grabber
    arm: Arm

    autobalance: AutoBalance
    drivetrain: DriveTrain

    twitch = magicbot.tunable(0.5)

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

        self.encoder_l = wpilib.Encoder(2, 3)
        self.encoder_r = wpilib.Encoder(0, 1)
        self.encoder_l.setDistancePerPulse(constants.kDistancePerPulse)
        self.encoder_r.setDistancePerPulse(constants.kDistancePerPulse)
        self.encoder_r.setReverseDirection(True)

        # Gyro
        self.ahrs = navx.AHRS.create_spi()

        # Arm
        self.arm_motor = CANSparkMax(6, CANSparkMax.MotorType.kBrushless)
        self.arm_motor2 = CANSparkMax(7, CANSparkMax.MotorType.kBrushless)

        # Grabber
        self.grabber_motor = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        self.grabber_sensor = SharpIR2Y0A41(0)

    @magicbot.feedback
    def left_encoder(self) -> int:
        return self.encoder_l.get()

    @magicbot.feedback
    def right_encoder(self) -> int:
        return self.encoder_r.get()

    @magicbot.feedback
    def left_encoder_d(self) -> int:
        return self.encoder_l.getDistance()

    @magicbot.feedback
    def right_encoder_d(self) -> int:
        return self.encoder_r.getDistance()

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        # drivetrain logic goes first
        speed = -self.stick.getEnhY()
        rotation = -self.stick.getEnhTwist() * abs(self.twitch)

        if self.stick.getRawButton(4):
            self.autobalance.overcome()
        elif self.stick.getRawButton(3):
            self.autobalance.maintain()

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
