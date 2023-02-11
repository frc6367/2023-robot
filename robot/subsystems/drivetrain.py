import wpilib.drive
import ctre
import magicbot


class DriveTrain:
    frontLeftMotor: ctre.WPI_TalonSRX
    rearLeftMotor: ctre.WPI_TalonSRX
    frontRightMotor: ctre.WPI_TalonSRX
    rearRightMotor: ctre.WPI_TalonSRX

    speed = magicbot.will_reset_to(0)
    rotation = magicbot.will_reset_to(0)

    def setup(self):
        self.drive = wpilib.drive.DifferentialDrive(
            self.frontLeftMotor,
            self.rearLeftMotor,
            self.frontRightMotor,
            self.rearRightMotor,
        )

    def move(self, speed: float, rotation: float):
        self.speed = speed
        self.rotation = rotation
