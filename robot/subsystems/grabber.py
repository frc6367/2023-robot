import magicbot
import rev
from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A41


class Grabber:
    motor: rev.CANSparkMax
    sensor: SharpIR2Y0A41

    #
    # Action methods
    #

    grab_current = magicbot.tunable(0.0)
    grab_current_avg = magicbot.tunable(0.0)

    grab_open_speed = magicbot.tunable(0.2)
    grab_close_speed = magicbot.tunable(-0.4)
    grab_position = magicbot.tunable(0.0)
    grab_threshold = magicbot.tunable(40.0)

    grab_state = magicbot.tunable("opened")

    def setup(self):
        self.encoder = self.motor.getEncoder()

        self.pid = self.motor.getPIDController()
        

        # Set PID Constants
        self.pid.setP(1)
        self.pid.setI(0)
        self.pid.setD(0)
        self.pid.setIZone(0)
        self.pid.setFF(0)
        self.pid.setOutputRange(-0.3, 0.3)

    def grab(self):
        if self.grab_state != "closed":
            self.grab_state = "closing"

    def release(self):
        if self.grab_state != "opened":
            self.grab_state = "opening"

    #
    # Feedback mathods
    #

    @magicbot.feedback
    def ball_distance(self):
        return self.sensor.getDistance()

    # @magicbot.feedback
    # def hasObject(self):
    #     pass

    @magicbot.feedback
    def isOpen(self):
        return self.grab_state == "opened"

    @magicbot.feedback
    def isClosed(self):
        return self.grab_state == "closed"

    @magicbot.feedback
    def isObjectSensed(self):
        return self.ball_distance() <= 9

    #
    # Execute
    #

    def execute(self):
        self.grab_current = self.motor.getOutputCurrent()
        self.grab_current_avg = (self.grab_current_avg * 0.92) + (
            (1 - 0.92) * self.grab_current
        )

        if self.grab_state == "closed":
            # self.pid.setReference(
            #     self.grab_position, rev.CANSparkMax.ControlType.kPosition
            # )
            self.motor.set(-0.1)
            # self.pid.setReference(0.1, rev.CANSparkMax.ControlType.kCurrent)
        elif self.grab_state == "closing":
            self.motor.set(self.grab_close_speed)
            if self.grab_current_avg > self.grab_threshold:
                self.grab_state = "closed"
                self.grab_position = self.encoder.getPosition()
                print("Closed")
        elif self.grab_state == "opened":
            self.motor.set(0)
        elif self.grab_state == "opening":
            self.motor.set(self.grab_open_speed)
            if self.grab_current_avg > self.grab_threshold:
                self.grab_state = "opened"
                print("Opened")
