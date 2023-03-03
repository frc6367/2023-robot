#
# See the notes for the other physics sample
#

import math
import numpy

import wpilib
import wpilib.simulation

import wpimath.controller
import wpimath.geometry
import wpimath.system
import wpimath.system.plant

from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

import typing

if typing.TYPE_CHECKING:
    from robot import MyRobot

from misc.sparksim import CANSparkMax

import constants


class PhysicsEngine:
    """
    Simulates a 4-wheel robot using Tank Drive joystick control
    """

    def __init__(self, physics_controller: PhysicsInterface, robot: "MyRobot"):
        """
        :param physics_controller: `pyfrc.physics.core.Physics` object
                                   to communicate simulation effects to
        :param robot: your robot object
        """

        self.physics_controller = physics_controller

        # Drivetrain simulation
        self.lf_motor = robot.drive_l1.getSimCollection()
        # self.lr_motor = wpilib.simulation.PWMSim(2)
        self.rf_motor = robot.drive_r1.getSimCollection()
        # self.rr_motor = wpilib.simulation.PWMSim(4)

        self.leftEncoderSim = wpilib.simulation.EncoderSim(robot.encoder_l)
        self.rightEncoderSim = wpilib.simulation.EncoderSim(robot.encoder_r)
        self.rightEncoderSim.setReverseDirection(True)

        system = wpimath.system.LinearSystemId.identifyDrivetrainSystem(
            constants.kV_linear,
            constants.kA_linear,
            constants.kV_angular,
            constants.kA_angular,
        )

        self.drivesim = wpilib.simulation.DifferentialDrivetrainSim(
            system,
            # The robot's trackwidth, which is the distance between the wheels on the left side
            # and those on the right side. The units is meters.
            constants.kTrackWidth,
            wpimath.system.plant.DCMotor.CIM(4),
            10.71,
            # The radius of the drivetrain wheels in meters.
            constants.kWheelRadius,
        )

        self.drivesim.setPose(constants.kStartingPose)
        self.physics_controller.field.setRobotPose(constants.kStartingPose)
        self.gyro_offset = constants.kStartingPose.rotation().degrees()

        self.navx = wpilib.simulation.SimDeviceSim("navX-Sensor[4]")
        self.navx_yaw = self.navx.getDouble("Yaw")

        # self.physics_controller.move_robot(wpimath.geometry.Transform2d(5, 5, 0))

        # Arm simulation
        motor = wpimath.system.plant.DCMotor.NEO(2)
        self.armSim = wpilib.simulation.SingleJointedArmSim(
            motor,
            constants.kArmGearing,
            wpilib.simulation.SingleJointedArmSim.estimateMOI(
                constants.kArmLength,
                constants.kArmMass,
            ),
            constants.kArmLength,
            math.radians(-100),
            math.radians(90),
            True,
        )

        # Create a Mechanism2d display of an Arm
        self.mech2d = wpilib.Mechanism2d(60, 60)
        self.armBase = self.mech2d.getRoot("ArmBase", 30, 30)
        self.armTower = self.armBase.appendLigament(
            "Arm Tower", 30, -90, 6, wpilib.Color8Bit(wpilib.Color.kBlue)
        )
        self.arm = self.armBase.appendLigament(
            "Arm", 30, self.armSim.getAngle(), 6, wpilib.Color8Bit(wpilib.Color.kYellow)
        )

        # Put Mechanism to SmartDashboard
        wpilib.SmartDashboard.putData("Arm Sim", self.mech2d)

        self.arm_motor: CANSparkMax = robot.arm_motor
        self.arm_motor_sim = wpilib.simulation.PWMSim(self.arm_motor)

    def update_sim(self, now: float, tm_diff: float) -> None:
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """

        voltage = wpilib.simulation.RoboRioSim.getVInVoltage()

        # Simulate the drivetrain
        field = self.physics_controller.field
        # self.drivesim.setPose(field.getRobotPose())

        self.lf_motor.setBusVoltage(voltage)
        self.rf_motor.setBusVoltage(voltage)
        # drivetrain always wants to drive to the left
        l_voltage = self.lf_motor.getMotorOutputLeadVoltage() * 0.95
        r_voltage = -self.rf_motor.getMotorOutputLeadVoltage()

        # Apply kS

        # .. this doesn't work
        # kS_linear = self.kS_linear
        # kS_angular = self.kS_angular
        # if abs(l_voltage - r_voltage) > kS_linear:
        #     kS = kS_angular
        # else:
        #     kS = kS_linear

        kS = constants.kS_linear

        if l_voltage > kS:
            l_voltage -= kS
        elif l_voltage < -kS:
            l_voltage += kS
        else:
            l_voltage = 0

        if r_voltage > kS:
            r_voltage -= kS
        elif r_voltage < -kS:
            r_voltage += kS
        else:
            r_voltage = 0

        self.drivesim.setInputs(l_voltage, r_voltage)
        self.drivesim.update(tm_diff)

        self.leftEncoderSim.setDistance(self.drivesim.getLeftPosition())
        self.leftEncoderSim.setRate(self.drivesim.getLeftVelocity())
        self.rightEncoderSim.setDistance(self.drivesim.getRightPosition())
        self.rightEncoderSim.setRate(self.drivesim.getRightVelocity())

        pose = self.drivesim.getPose()
        field.setRobotPose(pose)

        # Update the gyro simulation
        # -> FRC gyros are positive clockwise, but the returned pose is positive
        #    counter-clockwise
        # self.gyro.setAngle(-pose.rotation().degrees())
        self.navx_yaw.set(-pose.rotation().degrees() + self.gyro_offset)

        # Update the arm
        self.armSim.setInputVoltage(self.arm_motor_sim.getSpeed() * voltage)
        self.armSim.update(tm_diff)

        arm_angle = self.armSim.getAngleDegrees()
        # -90 is 0 for the encoder, 0 is 50
        self.arm_motor._encoder._position = (arm_angle + 90) * (50 / 90)
        self.arm.setAngle(arm_angle)
