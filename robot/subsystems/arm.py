import magicbot
import wpilib.drive
import rev


<<<<<<< Updated upstream
class Arm:
    arm_motor: rev.CANSparkMax
    arm_motor2: rev.CANSparkMax

    HI_MIN = 6
    HI_MAX = 7

    MID_MIN = 4
    MID_MAX = 5

    LOW_MIN = 2
    LOW_MAX = 3

    NETURAL_MIN = 0
    NETURAL_MAX = 1

    def createObjects(self):

        self.arm_motor2.follow(self.arm_motor, invert=True)

        self.encoder = self.arm_motor.getEncoder()

        # You must call getPIDController() on an existing CANSparkMax or
        # SparkMax object to fully use PID functionality
        self.pidController = self.arm_motor.getPIDController()

        self.kP = 0.1
        self.kI = 1e-4
        self.kD = 0
        self.kIz = 0
        self.kFF = 0
        self.kMinOutput = -1
        self.kMaxOutput = 1

        # The restoreFactoryDefaults() method can be used to reset the
        # configuration parameters in the SPARK MAX to their factory default
        # state. If no argument is passed, these parameters will not persist
        # between power cycles
        self.arm_motor.restoreFactoryDefaults()

        # Set PID Constants
        self.pidController.setP(self.kP)
        self.pidController.setI(self.kI)
        self.pidController.setD(self.kD)
        self.pidController.setIZone(self.kIz)
        self.pidController.setFF(self.kFF)
        self.pidController.setOutputRange(self.kMinOutput, self.kMaxOutput)

=======
>>>>>>> Stashed changes
    #
    # Action methods
    #

<<<<<<< Updated upstream
    def gotoHi(self):
        self.gotoAngle = 20

    def gotoMiddle(self):
        self.gotoAngle = 15

    def gotoLow(self):
        self.gotoAngle = 10

    def gotoNetural(self):
        self.gotoAngle = 5

    #
    # Feedback mathods
    #

    @magicbot.feedback
    def getAngle(self):
        encoder = self.arm_motor.getEncoder()

    @magicbot.feedback
    def getPosition(self):
        encoder = self.arm_motor.getEncoder()
        p = encoder.getPosition()
        if p > self.LOW_MIN and p < self.LOW_MAX:
            return "LOW"
        if p > self.MID_MIN and p < self.MID_MAX:
            return "MID"
        if p > self.HI_MIN and p < self.HI_MAX:
            return "HI"
        if p > self.NETURAL_MIN and p < self.NETURAL_MAX:
            return "NETURAL"
        return ""
=======
    def hi(self):
        pass
    def middle(self):
        pass
    def low(self):
        pass
    def netural(self):
        pass

    #
    # Feedback methods
    #

>>>>>>> Stashed changes

    #
    # Execute
    #

    def execute(self):
<<<<<<< Updated upstream
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
=======
        pass
    
    wpilib.SmartDashboard.
>>>>>>> Stashed changes
