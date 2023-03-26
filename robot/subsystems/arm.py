import math

import magicbot

from misc.led_controller import LEDController
from misc.sparksim import CANSparkMax

# NINETY_RAD = math.radians(90)


class Arm:
    arm_motor: CANSparkMax
    arm_motor2: CANSparkMax

    led: LEDController

    HI_POS = 62
    HI_MIN = HI_POS - 2
    HI_MAX = HI_POS + 2

    HI2_POS = 59
    HI2_MIN = HI2_POS - 2
    HI2_MAX = HI2_POS + 2

    MID_POS = 58
    MID_MIN = MID_POS - 2
    MID_MAX = MID_POS + 2

    MID2_POS = 47
    MID2_MIN = MID2_POS - 3
    MID2_MAX = MID2_POS + 3

    LOW_POS = 19
    LOW_MIN = LOW_POS - 2
    LOW_MAX = LOW_POS + 2

    OUT_POS = 10
    OUT_MIN = OUT_POS - 2
    OUT_MAX = OUT_POS + 2

    NEUTRAL_POS = 3
    NEUTRAL_MIN = NEUTRAL_POS - 2
    NEUTRAL_MAX = NEUTRAL_POS + 2

    def setup(self):
        self.arm_encoder = self.arm_motor.getEncoder()

        self.arm_motor2.follow(self.arm_motor, True)

        self.pidController = self.arm_motor.getPIDController()

        self.kP = 0.2
        self.kI = 0
        self.kD = 0.01
        self.kIz = 0
        self.kFF = 0
        self.kMinOutput = -0.4
        self.kMaxOutput = 0.4

        self.gotoAngle = 0

        self.arm_motor.restoreFactoryDefaults()

        # Set PID Constants
        self.pidController.setP(self.kP)
        self.pidController.setI(self.kI)
        self.pidController.setD(self.kD)
        self.pidController.setIZone(self.kIz)
        self.pidController.setFF(self.kFF)
        self.pidController.setOutputRange(self.kMinOutput, self.kMaxOutput)

    # @magicbot.feedback
    # def getAngleRad(self):
    #     return self.arm_encoder.getPosition() - NINETY_RAD

    # @magicbot.feedback
    # def getAngle(self) -> float:
    #     return math.degrees(self.getAngleRad())

    @magicbot.feedback
    def encoder_pos(self):
        return self.arm_encoder.getPosition()

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

    def gotoHi2(self):
        self.gotoAngle = self.HI2_POS

    #
    # Feedback mathods
    #

    # @magicbot.feedback
    # def getAngle(self):
    #     encoder = self.arm_motor.getEncoder()

    @magicbot.feedback
    def getPosition(self):
        p = self.arm_encoder.getPosition()
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

    def execute(self):
        # PIDController objects are commanded to a set point using the
        # setReference() method.
        #
        # The first parameter is the value of the set point, whose units vary
        # depending on the control type set in the second parameter.
        #
        # The second parameter is the control type can be set to one of four
        # parameters:
        # rev.CANSparkMax.ControlType.kDutyCycle
        # rev.CANSparkMax.ControlType.kPosition
        # rev.CANSparkMax.ControlType.kVelocity
        # rev.CANSparkMax.ControlType.kVoltage
        #
        # For more information on what these types are, refer to the Spark Max
        # documentation.
        self.pidController.setReference(
            self.gotoAngle, CANSparkMax.ControlType.kPosition
        )

        if self.arm_encoder.getPosition() > self.OUT_MIN:
            self.led.indicateArmUp()
