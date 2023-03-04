import magicbot
import wpilib.drive
import rev


class Arm:
    arm_motor: rev.CANSparkMax
    arm_motor2: rev.CANSparkMax

    HI_POS = 66
    HI_MIN = HI_POS - 2
    HI_MAX = HI_POS + 2

    MID_POS = 53
    MID_MIN = MID_POS - 2
    MID_MAX = MID_POS + 2

    LOW_POS = 19
    LOW_MIN = LOW_POS - 2
    LOW_MAX = LOW_POS + 2

    Out_Pos = 10
    Out_MIN = Out_Pos - 2
    Out_MAX = Out_Pos + 2

    NEUTRAL_POS = 3
    NEUTRAL_MIN = NEUTRAL_POS - 2
    NEUTRAL_MAX = NEUTRAL_POS + 2

    def setup(self):
        self.arm_encoder = self.arm_motor.getEncoder()

        self.arm_motor2.follow(self.arm_motor, True)

        self.pidController = self.arm_motor.getPIDController()

        self.kP = 0.1
        self.kI = 0
        self.kD = 0
        self.kIz = 0
        self.kFF = 0
        self.kMinOutput = -0.3
        self.kMaxOutput = 0.3

        self.gotoAngle = 0

        self.arm_motor.restoreFactoryDefaults()

        # Set PID Constants
        self.pidController.setP(self.kP)
        self.pidController.setI(self.kI)
        self.pidController.setD(self.kD)
        self.pidController.setIZone(self.kIz)
        self.pidController.setFF(self.kFF)
        self.pidController.setOutputRange(self.kMinOutput, self.kMaxOutput)

    def gotoHi(self):
        self.gotoAngle = self.HI_POS

    def gotoMiddle(self):
        self.gotoAngle = self.MID_POS

    def gotoLow(self):
        self.gotoAngle = self.LOW_POS

    def gotoOut(self):
        self.gotoAngle = self.Out_Pos

    def gotoNeutral(self):
        self.gotoAngle = self.NEUTRAL_POS

    #
    # Feedback mathods
    #

    # @magicbot.feedback
    # def getAngle(self):
    #     encoder = self.arm_motor.getEncoder()

    @magicbot.feedback
    def getPosition(self):
        p = self.arm_encoder.getPosition()
        if p > self.LOW_MIN and p < self.LOW_MAX:
            return "LOW"
        if p > self.MID_MIN and p < self.MID_MAX:
            return "MID"
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
            self.gotoAngle, rev.CANSparkMax.ControlType.kPosition
        )
