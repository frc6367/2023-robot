import magicbot

import navx
from wpimath.controller import PIDController

from subsystems.drivetrain import DriveTrain


class AutoBalance:
    ahrs: navx.AHRS
    drivetrain: DriveTrain

    active = magicbot.will_reset_to(False)

    kP = magicbot.tunable(0.3)
    maxOutMaintain = magicbot.tunable(0.2)
    maxOutOvercome = magicbot.tunable(0.31)
    maxR = magicbot.tunable(0.2)

    # Note to self: +/- 5% should be ok for autobalance??
    fwd_angle = magicbot.tunable(2.5)
    rev_angle = magicbot.tunable(-3)

    extra = magicbot.will_reset_to(0)

    def setup(self):
        self.pid = PIDController(self.kP, 0, 0)
        self.pid.setSetpoint(0)
        self.was_active = False

        turnController = PIDController(
            0.03,
            0,
            0.0,
        )
        turnController.enableContinuousInput(-180.0, 180.0)
        turnController.setTolerance(2)
        self.turnController = turnController

    def maintain(self):
        self._activate(self.maxOutMaintain)

    def overcome(self, n):
        self.extra = n
        self.maintain()

    def _activate(self, maxOut):
        self.active = True
        self.maxOut = maxOut

        if not self.was_active:
            self.pid.reset()
            self.pid.setP(self.kP)

            self.turnController.reset()
            self.turnController.setSetpoint(self.ahrs.getYaw())

    @magicbot.feedback
    def get_angle(self):
        return self.ahrs.getRoll()

    @magicbot.feedback
    def get_yaw(self):
        return self.ahrs.getYaw()

    def execute(self):
        if self.active:
            angle = self.get_angle()

            if angle > self.fwd_angle or angle < self.rev_angle:
                if angle > self.fwd_angle:
                    angle -= self.fwd_angle
                # else:
                #     angle -= self.rev_angle

                speed = self.pid.calculate(angle) + self.extra
                maxOut = abs(self.maxOut)
                if speed > maxOut:
                    speed = maxOut
                elif speed < -maxOut:
                    speed = -maxOut

                rotation = -self.turnController.calculate(self.ahrs.getYaw())
                maxR = abs(self.maxR)
                if rotation > maxR:
                    rotation = maxR
                elif rotation < -maxR:
                    rotation = -maxR

                self.drivetrain.move(speed, rotation)

        self.was_active = self.active
