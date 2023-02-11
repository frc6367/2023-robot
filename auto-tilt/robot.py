#!/usr/bin/env python3

import wpilib
import wpilib.drive
import wpimath.controller
import ctre
import navx
import rev

from navx import AHRS

# from misc.sparksim import CANSparkMax


class MyRobot(wpilib.TimedRobot):
    """This is a demo program showing the use of the navX MXP to implement
    a "rotate to angle" feature. This demo works in the pyfrc simulator.
    This example will automatically rotate the robot to one of four
    angles (0, 90, 180 and 270 degrees).
    This rotation can occur when the robot is still, but can also occur
    when the robot is driving.  When using field-oriented control, this
    will cause the robot to drive in a straight line, in whatever direction
    is selected.
    This example also includes a feature allowing the driver to "reset"
    the "yaw" angle.  When the reset occurs, the new gyro angle will be
    0 degrees.  This can be useful in cases when the gyro drifts, which
    doesn't typically happen during a FRC match, but can occur during
    long practice sessions.
    Note that the PID Controller coefficients defined below will need to
    be tuned for your drive system.
    """

    # The following PID Controller coefficients will need to be tuned */
    # to match the dynamics of your drive system.  Note that the      */
    # SmartDashboard in Test mode has support for helping you tune    */
    # controllers by displaying a form where you can enter new P, I,  */
    # and D constants and test the mechanism.                         */

    # Often, you will find it useful to have different parameters in
    # simulation than what you use on the real robot

    if wpilib.RobotBase.isSimulation():
        # These PID parameters are used in simulation
        kP = 0.03
        kI = 0.00
        kD = 0.00
    else:
        # These PID parameters are used on a real robot
        kP = 0.001
        kI = 0.00
        kD = 0.00

    kToleranceDegrees = 1.0

    def robotInit(self):
        # Channels for the wheels
        self.frontLeftMotor = ctre.WPI_TalonSRX(4)
        self.rearLeftMotor = ctre.WPI_TalonSRX(3)
        self.frontRightMotor = ctre.WPI_TalonSRX(1)
        self.rearRightMotor = ctre.WPI_TalonSRX(2)

        self.frontRightMotor.setInverted(True)
        self.rearRightMotor.setInverted(True)

        self.left = wpilib.MotorControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.MotorControllerGroup(
            self.frontRightMotor, self.rearRightMotor
        )

        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        # self.myRobot.setExpiration(0.1)

        self.stick = wpilib.Joystick(0)
        #self.sticks = wpilib.Joystick(1)

        #
        # Communicate w/navX MXP via the MXP SPI Bus.
        # - Alternatively, use the i2c bus.
        # See http://navx-mxp.kauailabs.com/guidance/selecting-an-interface/ for details
        #
        self.gyro = navx.AHRS.create_spi()

        # self.ahrs = AHRS.create_spi()
        # self.ahrs = AHRS.create_i2c()

        turnController = wpimath.controller.PIDController(
            self.kP,
            self.kI,
            self.kD,
        )
        # turnController.enableContinuousInput(-180.0, 180.0)
        turnController.setTolerance(self.kToleranceDegrees)

        wpilib.SmartDashboard.putNumber("auto_p", self.kP)
        wpilib.SmartDashboard.putNumber("auto_D", self.kD)

        self.tiltController = turnController

        self.intakem = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        #self.intakems = rev.CANSparkMax(6, rev.CANSparkMax.MotorType.kBrushless)

    def teleopInit(self):
        self.tm = wpilib.Timer()
        self.tm.start()

    def teleopPeriodic(self):
        """Runs the motors with onnidirectional drive steering.
        Implements Field-centric drive control.
        Also implements "rotate to angle", where the angle
        being rotated to is defined by one of four buttons.
        Note that this "rotate to angle" approach can also
        be used while driving to implement "straight-line
        driving".
        """
        self.intakem.set(self.stick.getZ())
       # self.intakems.set(self.sticks.getZ())

        if self.tm.advanceIfElapsed(1.0):
            print("NavX Gyro", self.gyro.getRoll(), self.gyro.getAngle())

        auto_balance = False
        if self.stick.getRawButton(2):
            self.gyro.reset()

        if self.stick.getRawButton(1):

            auto_balance = True
        # if self.stick.getRawButton(3):
        #    self.intakem.set(1.0)
            # self.stick = rev.CANSparkMax(1, rev.CANSparkMax.MotorType.kBrushless)
            # self.intake.motor.setvoltage()
        if auto_balance:
            speed = self.tiltController.calculate(self.gyro.getRoll(), 0)
            rotation = 0
            squared = False
        else:
            self.tiltController.reset()
            self.tiltController.setP(wpilib.SmartDashboard.getNumber("auto_p", self.kP))
            self.tiltController.setD(wpilib.SmartDashboard.getNumber("auto_d", self.kD))

            speed = -self.stick.getY()
            rotation = -self.stick.getZ()
            squared = True

        # Use the joystick Y axis for forward movement,
        # and either the X axis for rotation or the current
        # calculated rotation rate depending upon whether
        # "rotate to angle" is active.
        #
        # This works better for mecanum drive robots, but this
        # illustrates one way you could implement this using
        # a 4 wheel drive robot

        self.drive.arcadeDrive(speed, rotation, squared)


if __name__ == "__main__":
    wpilib.run(MyRobot)
