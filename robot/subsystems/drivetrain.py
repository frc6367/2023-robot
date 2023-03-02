import wpilib.drive
import ctre
import magicbot
import wpimath.controller
from wpimath.trajectory.constraint import DifferentialDriveKinematicsConstraint


class DriveTrain:
    drive_l1: ctre.WPI_TalonSRX
    drive_l2: ctre.WPI_TalonSRX
    drive_r1: ctre.WPI_TalonSRX
    drive_r2: ctre.WPI_TalonSRX

    speed = magicbot.will_reset_to(0)
    rotation = magicbot.will_reset_to(0)
    limit = magicbot.will_reset_to(1.0)

    l = magicbot.will_reset_to(0.0)
    r = magicbot.will_reset_to(0.0)
    tank = magicbot.will_reset_to(False)

    def setup(self):
        # self.drive_l1.setInverted(True)
        # self.drive_l2.setInverted(True)

        self.drive_l2.follow(self.drive_l1)
        self.drive_r2.follow(self.drive_r1)

        self.drive = wpilib.drive.DifferentialDrive(self.drive_l1, self.drive_r1)

        # self.l_pid = wpimath.controller.ProfiledPIDController(0.1, 0, 0, self.constraints)
        # self.r_pid = wpimath.controller.ProfiledPIDController()

    def limit_speed(self):
        self.limit = 0.5

    def move(self, speed: float, rotation: float):
        self.speed = speed
        self.rotation = rotation

    def tank_drive(self, l, r):
        self.tank = True
        self.l = l
        self.r = r

    def rotate(self, rotation: float):
        self.rotation = rotation

    def move_encoder_stright(self, position):
        raise NotImplemented

    def is_at_desired_position(self):
        raise NotImplemented

    def move_encoder_backwards(self):
        raise NotImplemented

    def execute(self):
        if self.tank:
            self.drive.tankDrive(self.l, self.r)
        else:
            self.drive.arcadeDrive(
                self.speed * self.limit, self.rotation * self.limit, False
            )
