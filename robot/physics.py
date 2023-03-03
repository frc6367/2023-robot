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

        # Motors
        self.lf_motor = robot.drive_l1.getSimCollection()
        # self.lr_motor = wpilib.simulation.PWMSim(2)
        self.rf_motor = robot.drive_r1.getSimCollection()
        # self.rr_motor = wpilib.simulation.PWMSim(4)

        # Change these parameters to fit your robot!
        bumper_width = 3.25 * units.inch

        # fmt: off
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,           # motor configuration
            110 * units.lbs,                    # robot mass
            10.71,                              # drivetrain gear ratio
            2,                                  # motors per side
            22 * units.inch,                    # robot wheelbase
            23 * units.inch + bumper_width * 2, # robot width
            32 * units.inch + bumper_width * 2, # robot length
            6 * units.inch,                     # wheel diameter
        )
        # fmt: on

        self.navx = wpilib.simulation.SimDeviceSim("navX-Sensor[4]")
        self.navx_yaw = self.navx.getDouble("Yaw")

        self.physics_controller.move_robot(wpimath.geometry.Transform2d(5, 5, 0))

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

        # Simulate the drivetrain (only front motors used because read should be in sync)
        lf_motor = self.lf_motor.getMotorOutputLeadVoltage() / 12
        rf_motor = self.rf_motor.getMotorOutputLeadVoltage() / 12

        transform = self.drivetrain.calculate(lf_motor, rf_motor, tm_diff)
        pose = self.physics_controller.move_robot(transform)

        # Update the gyro simulation
        # -> FRC gyros are positive clockwise, but the returned pose is positive
        #    counter-clockwise
        # self.gyro.setAngle(-pose.rotation().degrees())
        self.navx_yaw.set(-pose.rotation().degrees())

        # Update the arm
        self.armSim.setInputVoltage(self.arm_motor_sim.getSpeed() * voltage)
        self.armSim.update(tm_diff)

        arm_angle = self.armSim.getAngleDegrees()
        # -90 is 0 for the encoder, 0 is 50
        self.arm_motor._encoder._position = (arm_angle + 90) * (50 / 90)
        self.arm.setAngle(arm_angle)
