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

        self.encoder1 = wpilib.Encoder(0, 1)
        self.encoder2 = wpilib.Encoder(2, 3)

        self.setupArm()
        self.setupGrabber()

        # joysticks 1 & 2 on the driver station
        self.stick = wpilib.Joystick(0)

    def setupGrabber(self):
        self.grabber = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        self.grabEncoder = self.grabber.getEncoder()

        self.grab_state = "opened"
        self.grab_open_speed = 0.2
        self.grab_close_speed = -0.4
        self.grab_position = 0
        self.grab_threshold = 40
        self.grab_current_avg = 0

        self.grabPid = self.grabber.getPIDController()

        # Set PID Constants
        self.grabPid.setP(1)
        self.grabPid.setI(0)
        self.grabPid.setD(0)
        self.grabPid.setIZone(0)
        self.grabPid.setFF(0)
        self.grabPid.setOutputRange(-0.3, 0.3)

    def setupArm(self):
        self.arm_motor = rev.CANSparkMax(6, rev.CANSparkMax.MotorType.kBrushless)
        self.arm2 = rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)

        self.arm_encoder = self.arm_motor.getEncoder()

        self.arm2.follow(self.arm_motor, True)

        self.pidController = self.arm_motor.getPIDController()

        self.kP = 0.1
        self.kI = 0
        self.kD = 0
        self.kIz = 0
        self.kFF = 0
        self.kMinOutput = -0.3
        self.kMaxOutput = 0.3

        self.goto_angle = 0

        self.arm_motor.restoreFactoryDefaults()

        # Set PID Constants
        self.pidController.setP(self.kP)
        self.pidController.setI(self.kI)
        self.pidController.setD(self.kD)
        self.pidController.setIZone(self.kIz)
        self.pidController.setFF(self.kFF)
        self.pidController.setOutputRange(self.kMinOutput, self.kMaxOutput)

    def teleopInit(self) -> None:
        print("In teleopInit")

    def teleopPeriodic(self):
        wpilib.SmartDashboard.putNumber("curent", self.grabber.getOutputCurrent())
        wpilib.SmartDashboard.putNumber("speed", self.stick.getRawAxis(3))
        wpilib.SmartDashboard.putNumber(
            "Grabber-encoder", self.grabEncoder.getPosition()
        )
        wpilib.SmartDashboard.putNumber(
            "arm_motor-encoder", self.arm_encoder.getPosition()
        )

        # if self.stick.getRawButton(1):
        #     self.grabber.set(self.stick.getRawAxis(3))
        # elif self.stick.getRawButton(2):
        #     self.grabber.set(-self.stick.getRawAxis(3))
        # else:
        #     self.grabber.set(0)

        if self.stick.getRawButton(1):
            if self.grab_state != "closed":
                self.grab_state = "closing"
        elif self.stick.getRawButton(2):
            if self.grab_state != "opened":
                self.grab_state = "opening"

        self.grab_current = self.grabber.getOutputCurrent()
        self.grab_current_avg = (self.grab_current_avg * 0.92) + (
            (1 - 0.92) * self.grab_current
        )

        if self.grab_state == "closed":
            self.grabPid.setReference(
                self.grab_position, rev.CANSparkMax.ControlType.kPosition
            )
        elif self.grab_state == "closing":
            self.grabber.set(self.grab_close_speed)
            if self.grab_current_avg > self.grab_threshold:
                self.grab_state = "closed"
                self.grab_position = self.grabEncoder.getPosition()
                print("Closed")
        elif self.grab_state == "opened":
            self.grabber.set(0)
        elif self.grab_state == "opening":
            self.grabber.set(self.grab_open_speed)
            if self.grab_current_avg > self.grab_threshold:
                self.grab_state = "opened"
                print("Opened")

        if self.stick.getRawButton(7):
            self.goto_angle = 56
        elif self.stick.getRawButton(9):
            self.goto_angle = 43
        elif self.stick.getRawButton(11):
            self.goto_angle = 19
        elif self.stick.getRawButton(12):
            self.goto_angle = 0

        self.pidController.setReference(
            self.goto_angle, rev.CANSparkMax.ControlType.kPosition
        )

        wpilib.SmartDashboard.putNumber("grab-current", self.grab_current)
        wpilib.SmartDashboard.putNumber("grab-pos", self.grab_position)
        wpilib.SmartDashboard.putString("grab-state", self.grab_state)
        wpilib.SmartDashboard.putNumber("grab-current-avg", self.grab_current_avg)

        wpilib.SmartDashboard.putNumber("e1", self.encoder1.get())
        wpilib.SmartDashboard.putNumber("e2", self.encoder2.get())


if __name__ == "__main__":
    wpilib.run(MyRobot)
