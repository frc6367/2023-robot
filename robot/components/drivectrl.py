import magicbot

import wpilib
import wpimath.controller
from wpimath.trajectory import TrapezoidProfile

from subsystems.drivetrain import DriveTrain


class DriveController:
    drivetrain: DriveTrain
    encoder_l: wpilib.Encoder
    encoder_r: wpilib.Encoder

    active = magicbot.will_reset_to(False)

    def setup(self):
        self.was_active = False

        self.constraints = TrapezoidProfile.Constraints(6, 0.5)

        self.l_pid = wpimath.controller.ProfiledPIDController(
            8.5, 0, 0, self.constraints
        )
        self.r_pid = wpimath.controller.ProfiledPIDController(
            8.5, 0, 0, self.constraints
        )

        self.l_pid.setTolerance(0.01)
        self.r_pid.setTolerance(0.01)

    def straight(self, N: float):
        if not self.was_active:
            self.encoder_l.reset()
            self.encoder_r.reset()

            self.l_goal = N
            self.r_goal = N

            self.l_pid.reset(0, 0)
            self.r_pid.reset(0, 0)

        self.active = True

    @magicbot.feedback
    def at_goal(self) -> bool:
        return self.l_pid.atGoal() and self.r_pid.atGoal()

    def execute(self):
        if self.active:
            self.drivetrain.tank_drive(
                self.l_pid.calculate(self.encoder_l.getDistance(), self.l_goal),
                self.r_pid.calculate(self.encoder_l.getDistance(), self.r_goal),
            )

        self.was_active = self.active
