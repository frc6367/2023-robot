import math
import wpilib
import magicbot

import navx
from wpimath.controller import PIDController

from subsystems.drivetrain import DriveTrain


class AutoBalance:
    ahrs: navx.AHRS
    kP = magicbot.tunable(0.1)
    maxOutMaintain = magicbot.tunable(0.15)
    maxOutOvercome = magicbot.tunable(0.31)
    maxR = magicbot.tunable(0.2)
    drivetrain: DriveTrain

    active = magicbot.will_reset_to(False)

    def __init__(self):
        self.mRioAccel = wpilib.BuiltInAccelerometer()

        self.state = 0
        self.debounceCount = 0

        ##########
        # CONFIG #
        ##########

        # Speed the robot drived while scoring/approaching station, default = 0.4
        self.robotSpeedFast = 0.4

        # Speed the robot drives while balancing itself on the charge station.
        # Should be roughly half the fast speed, to make the robot more accurate, default = 0.2
        self.robotSpeedSlow = 0.2

        # Angle where the robot knows it is on the charge station, default = 13.0
        self.onChargeStationDegree = 13.0

        # Angle where the robot can assume it is level on the charging station
        # Used for exiting the drive forward sequence as well as for auto balancing, default = 6.0
        self.levelDegree = 6.0

        # Amount of time a sensor condition needs to be met before changing states in seconds
        # Reduces the impact of sensor noice, but too high can make the auto run slower, default = 0.2
        self.debounceTime = 0.2

        # # Amount of time to drive towards to scoring target when trying to bump the game piece off
        # # Time it takes to go from starting position to hit the scoring target
        # self.singleTapTime = 0.4

        # # Amount of time to drive away from knocked over gamepiece before the second tap
        # self.scoringBackUpTime = 0.2

        # # Amount of time to drive forward to secure the scoring of the gamepiece
        # self.doubleTapTime = 0.3

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

    def getPitch(self) -> float:
        return (
            math.atan2(
                (-self.mRioAccel.getX()),
                math.sqrt(
                    self.mRioAccel.getY() * self.mRioAccel.getY()
                    + self.mRioAccel.getZ() * self.mRioAccel.getZ()
                ),
            )
            * 57.3
        )

    def getRoll(self) -> float:
        return math.atan2(self.mRioAccel.getY(), self.mRioAccel.getZ()) * 57.3

    def getTilt(self) -> float:
        """returns the magnititude of the robot's tilt calculated by the root of
        pitch^2 + roll^2, used to compensate for diagonally mounted rio
        """
        if (self.getPitch() + self.getRoll()) >= 0:
            return math.sqrt(
                self.getPitch() * self.getPitch() + self.getRoll() * self.getRoll()
            )
        else:
            return -math.sqrt(
                self.getPitch() * self.getPitch() + self.getRoll() * self.getRoll()
            )

    def secondsToTicks(self, time: float) -> int:
        return int(time * 50)

    def autoBalanceRoutine(self) -> float:
        """
        routine for automatically driving onto and engaging the charge station.
        returns a value from -1.0 to 1.0, which left and right motors should be set to.
        """
        if self.state == 0:
            # drive forwards to approach station, exit when tilt is detected
            if self.getTilt() > self.onChargeStationDegree:
                self.debounceCount += 1

            if self.debounceCount > self.secondsToTicks(self.debounceTime):
                self.state = 1
                self.debounceCount = 0
                return self.robotSpeedSlow

            return self.robotSpeedFast

        elif self.state == 1:
            # driving up charge station, drive slower, stopping when level
            if self.getTilt() < self.levelDegree:
                self.debounceCount += 1

            if self.debounceCount > self.secondsToTicks(self.debounceTime):
                self.state = 2
                self.debounceCount = 0
                return 0

            return self.robotSpeedSlow

        elif self.state == 2:
            # on charge station, stop motors and wait for end of auto
            if abs(self.getTilt()) <= self.levelDegree / 2:
                self.debounceCount += 1

            if self.debounceCount > self.secondsToTicks(self.debounceTime):
                self.state = 4
                self.debounceCount = 0
                return 0

            if self.getTilt() >= self.levelDegree:
                return 0.1
            elif self.getTilt() <= -self.levelDegree:
                return -0.1

        else:
            return 0

    def execute(self):
        if self.getPitch and self.getRoll and self.getTilt and self.secondsToTicks:
            self.autoBalanceRoutine
        if self.active:
            angle = self.get_angle()

            if angle > self.fwd_angle or angle < self.rev_angle:
                if angle > self.fwd_angle:
                    angle -= self.fwd_angle
                # else:
                #     angle -= self.rev_angle

                speed = self.pid.calculate(angle)
                maxOut = abs(self.maxOut)
                if speed > maxOut:
                    speed = maxOut
                elif speed < -maxOut:
                    speed = -maxOut

                speed = speed + self.extra

                # rotation = -self.turnController.calculate(self.ahrs.getYaw())
                # maxR = abs(self.maxR)
                # if rotation > maxR:
                #     rotation = maxR
                # elif rotation < -maxR:
                #     rotation = -maxR

                self.drivetrain.move(speed, 0)

        self.was_active = self.active


# import magicbot

# import navx
# from wpimath.controller import PIDController

# from subsystems.drivetrain import DriveTrain


# class AutoBalance:
#     ahrs: navx.AHRS
#     drivetrain: DriveTrain

#     active = magicbot.will_reset_to(False)

# kP = magicbot.tunable(0.1)
# maxOutMaintain = magicbot.tunable(0.15)
# maxOutOvercome = magicbot.tunable(0.31)
# maxR = magicbot.tunable(0.2)

#     # Note to self: +/- 5% should be ok for autobalance??
#     fwd_angle = magicbot.tunable(3)
#     rev_angle = magicbot.tunable(-3)

#     extra = magicbot.will_reset_to(0)

#     def setup(self):
#         self.pid = PIDController(self.kP, 0, 0)
#         self.pid.setSetpoint(0)
#         self.was_active = False

#         turnController = PIDController(
#             0.03,
#             0,
#             0.0,
#         )
#         turnController.enableContinuousInput(-180.0, 180.0)
#         turnController.setTolerance(2)
#         self.turnController = turnController

# def maintain(self):
#     self._activate(self.maxOutMaintain)

# def overcome(self, n):
#     self.extra = n
#     self.maintain()

# def _activate(self, maxOut):
#     self.active = True
#     self.maxOut = maxOut

#     if not self.was_active:
#         self.pid.reset()
#         self.pid.setP(self.kP)

#         self.turnController.reset()
#         self.turnController.setSetpoint(self.ahrs.getYaw())

#     @magicbot.feedback
#     def get_angle(self):
#         return self.ahrs.getRoll()

#     @magicbot.feedback
#     def get_yaw(self):
#         return self.ahrs.getYaw()

#     def execute(self):
#         if self.active:
#             angle = self.get_angle()

#             if angle > self.fwd_angle or angle < self.rev_angle:
#                 if angle > self.fwd_angle:
#                     angle -= self.fwd_angle
#                 # else:
#                 #     angle -= self.rev_angle

#                 speed = self.pid.calculate(angle)
#                 maxOut = abs(self.maxOut)
#                 if speed > maxOut:
#                     speed = maxOut
#                 elif speed < -maxOut:
#                     speed = -maxOut

#                 speed = speed + self.extra

#                 # rotation = -self.turnController.calculate(self.ahrs.getYaw())
#                 # maxR = abs(self.maxR)
#                 # if rotation > maxR:
#                 #     rotation = maxR
#                 # elif rotation < -maxR:
#                 #     rotation = -maxR

#                 self.drivetrain.move(speed, 0)

#         self.was_active = self.active
