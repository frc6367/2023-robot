import magicbot
import rev

import wpilib
from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A41


class Grabber:
    motor: rev.CANSparkMax
    sensor: SharpIR2Y0A41

    #
    # Action methods
    #

    grab_current = magicbot.tunable(0.0)
    grab_current_avg = magicbot.tunable(0.0)

    grab_open_speed = magicbot.tunable(0.1)
    grab_close_speed = magicbot.tunable(-1)
    grab_lower_open_speed = magicbot.tunable(1)
    grab_position = magicbot.tunable(0.0)
    grab_threshold = magicbot.tunable(40.0)

    # grab_state = magicbot.tunable("")

    speed = magicbot.will_reset_to(0)

    def setup(self):
        self.timer = wpilib.Timer()
        self.timer.start()
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
        # if self.grab_state != "closed":
        #     self.grab_state = "closing"
        self.speed = self.grab_close_speed

    def release(self, force=False):
        # if force or self.grab_state != "opened":
        #     self.grab_state = "begin_opening"
        self.speed = self.grab_open_speed

    def lower_release(self):
        self.speed = self.grab_lower_open_speed

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
    def isClosed(self):
        # return self.grab_state == "closed"
        return False

    @magicbot.feedback
    def isObjectSensed(self):
        return self.ball_distance() <= 12

    #
    # Execute
    #

    def execute(self):
        self.grab_current = self.motor.getOutputCurrent()
        self.grab_current_avg = (self.grab_current_avg * 0.92) + (
            (1 - 0.92) * self.grab_current
        )

        self.motor.set(self.speed)

        # if self.grab_state == "closed":
        #     # self.pid.setReference(
        #     #     self.grab_position, rev.CANSparkMax.ControlType.kPosition
        #     # )
        #     self.motor.set(-0.12)
        #     # self.pid.setReference(0.1, rev.CANSparkMax.ControlType.kCurrent)
        # elif self.grab_state == "closing":
        #     self.motor.set(self.grab_close_speed)
        #     if self.grab_current_avg > self.grab_threshold:
        #         self.grab_state = "closed"
        #         self.grab_position = self.encoder.getPosition()
        #         print("Closed")
        # elif self.grab_state == "opened":
        #     self.motor.set(0)
        # elif self.grab_state == "begin_opening":
        #     self.timer.reset()
        #     self.motor.set(self.grab_open_speed)
        #     self.grab_state = "opening"
        # elif self.grab_state == "opening":
        #     self.motor.set(self.grab_open_speed)
        #     if self.timer.get() > 0.2 and self.grab_current_avg > self.grab_threshold:
        #         self.grab_state = "opened"
        #         print("Opened")
