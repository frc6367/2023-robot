import math

import magicbot
import wpimath.controller
import wpimath.trajectory

import constants

from misc.sparksim import CANSparkMax

NINETY_RAD = math.radians(90)


class Arm:
    arm_motor: CANSparkMax
    arm_motor2: CANSparkMax

    HI_POS = math.radians(30)
    HI_MIN = HI_POS - math.radians(2)
    HI_MAX = HI_POS + math.radians(2)

    MID_POS = math.radians(7)
    MID_MIN = MID_POS - math.radians(2)
    MID_MAX = MID_POS + math.radians(2)

    MID2_POS = math.radians(-7)
    MID2_MIN = MID2_POS - math.radians(2)
    MID2_MAX = MID2_POS + math.radians(2)

    LOW_POS = math.radians(-60)
    LOW_MIN = LOW_POS - math.radians(2)
    LOW_MAX = LOW_POS + math.radians(2)

    OUT_POS = math.radians(-75)
    OUT_MIN = OUT_POS - math.radians(2)
    OUT_MAX = OUT_POS + math.radians(2)

    NEUTRAL_POS = math.radians(-87)
    NEUTRAL_MIN = NEUTRAL_POS - math.radians(2)
    NEUTRAL_MAX = NEUTRAL_POS + math.radians(2)

    gotoAngle = magicbot.tunable(NEUTRAL_POS)

    def setup(self):
        self.arm_motor.restoreFactoryDefaults()
        self.arm_encoder = self.arm_motor.getEncoder()
        # print("conversion", self.arm_encoder.getPositionConversionFactor())
        self.arm_encoder.setPositionConversionFactor(90 / 2800.0)

        self.arm_motor2.follow(self.arm_motor, True)

        self.last_kp = 0
        self.last_kd = 0

        self.pid_controller = wpimath.controller.ProfiledPIDController(
            constants.ArmConstants.kP,
            0,
            0,
            wpimath.trajectory.TrapezoidProfile.Constraints(
                constants.ArmConstants.kMaxVelocityRadPerSecond,
                constants.ArmConstants.kMaxAccelerationRadPerSecSquared,
            ),
        )

        # self.feedforward = wpimath.controller.ArmFeedforward(
        #     constants.ArmConstants.kSVolts,
        #     constants.ArmConstants.kGVolts,
        #     constants.ArmConstants.kVVoltSecondPerRad,
        #     constants.ArmConstants.kAVoltSecondSquaredPerRad,
        # )

    def on_enable(self):
        self.pid_controller.reset(self.getAngleRad())

    @magicbot.feedback
    def getAngleRad(self):
        return self.arm_encoder.getPosition() - NINETY_RAD

    @magicbot.feedback
    def getAngle(self) -> float:
        return math.degrees(self.getAngleRad())

    @magicbot.feedback
    def getGotoDeg(self) -> float:
        return math.degrees(self.gotoAngle)

    def gotoHi(self):
        self.gotoAngle = self.HI_POS

    def gotoMiddle(self):
        self.gotoAngle = self.MID_POS

    def gotoMiddle2(self):
        self.gotoAngle = self.MID2_POS

    def gotoLow(self):
        self.gotoAngle = self.LOW_POS

    def gotoOut(self):
        self.gotoAngle = self.OUT_POS

    def gotoNeutral(self):
        self.gotoAngle = self.NEUTRAL_POS

    #
    # Feedback mathods
    #

    @magicbot.feedback
    def getPosition(self):
        p = self.getAngleRad()
        return self._compute_pos(p)

    @magicbot.feedback
    def getGotoPosition(self):
        return self._compute_pos(self.gotoAngle)

    def _compute_pos(self, p):
        if p > self.OUT_MIN and p < self.OUT_MAX:
            return "OUT"
        if p > self.LOW_MIN and p < self.LOW_MAX:
            return "LOW"
        if p > self.MID_MIN and p < self.MID_MAX:
            return "MID"
        if p > self.MID2_MIN and p < self.MID2_MAX:
            return "MID2"
        if p > self.HI_MIN and p < self.HI_MAX:
            return "HI"
        if p > self.NEUTRAL_MIN and p < self.NEUTRAL_MAX:
            return "NEUTRAL"
        return ""

    #
    # Execute
    #

    kS = magicbot.tunable(0.0)
    kG = magicbot.tunable(0.4)
    kV = magicbot.tunable(1.0)
    kA = magicbot.tunable(0.0)

    kP = magicbot.tunable(4.5)
    kD = magicbot.tunable(1.0)

    RESET = magicbot.tunable(False)

    def execute(self):
        if self.RESET:
            self.arm_motor.set(-0.08)
            # self.arm_encoder.setPosition(0)
            return

        if abs(self.last_kp - self.kP) > 0.001:
            self.pid_controller.setP(self.kP)
            self.last_kp = self.kP

        if abs(self.last_kd - self.kD) > 0.001:
            self.pid_controller.setD(self.kD)
            self.last_kd = self.kD

        self.feedforward = wpimath.controller.ArmFeedforward(
            self.kS,
            self.kG,
            self.kV,
            self.kA,
        )

        state = self.pid_controller.getSetpoint()
        speed = self.pid_controller.calculate(self.getAngleRad(), self.gotoAngle)
        feedforward = self.feedforward.calculate(state.position, state.velocity)
        self.arm_motor.setVoltage(speed + feedforward)
