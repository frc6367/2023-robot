#!/usr/bin/env python3

import wpilib
import magicbot
from wpimath.filter import SlewRateLimiter

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

from components.auto_lifter import AutoLifter
from components.auto_grabber import AutoGrabber
from components.auto_balance import AutoBalance
from components.ramsete import RamseteComponent


class MyRobot(magicbot.MagicRobot):
    auto_lift: AutoLifter
    auto_grab: AutoGrabber
    grabber: Grabber
    arm: Arm

    ramsete: RamseteComponent
    autobalance: AutoBalance
    drivetrain: DriveTrain

    twitch_no_ball = magicbot.tunable(0.4)
    twitch_w_ball = magicbot.tunable(0.26)

    adjust = magicbot.tunable(0.3)

    def createObjects(self):
        # Joysticks
        self.stick = EnhancedJoystick(0)
        self.stick_limiter = SlewRateLimiter(3)

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
        self.arm_motor = CANSparkMax(7, CANSparkMax.MotorType.kBrushless)
        self.arm_motor2 = CANSparkMax(6, CANSparkMax.MotorType.kBrushless)

        # Grabber
        self.grabber_motor = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        self.grabber_sensor = SharpIR2Y0A41(0)
        self.grabber_motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)

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
        self.stick_limiter.reset(0)

    def teleopPeriodic(self):
        # drivetrain logic goes first
        if self.grabber.isClosed():
            twitch = self.twitch_w_ball
        else:
            twitch = self.twitch_no_ball

        speed1 = -self.stick.getEnhY()
        speed = self.stick_limiter.calculate(speed1)
        rotation = -self.stick.getEnhTwist() * abs(twitch)

        self.drivetrain.move(speed, rotation)

        if self.stick.getRawButton(3):
            self.autobalance.overcome(speed1 * self.adjust)
        # elif self.stick.getRawButton(4):
        #     self.autobalance.maintain()

        if self.stick.getRawButton(7):
            self.arm.gotoHi()
        elif self.stick.getRawButton(8):
            self.arm.gotoMiddle2()
        elif self.stick.getRawButton(9):
            self.arm.gotoMiddle()
        elif self.stick.getRawButton(11):
            self.arm.gotoLow()
        elif self.stick.getRawButton(12):
            self.arm.gotoOut()
        elif self.stick.getRawButton(10):
            self.arm.gotoNeutral()

        if self.stick.getRawButton(1):
            self.grabber.grab()
        elif self.stick.getRawButton(2):
            self.grabber.release()
        else:
            # self.auto_grab.activate()
            self.auto_lift.activate()


if __name__ == "__main__":
    wpilib.run(MyRobot)
