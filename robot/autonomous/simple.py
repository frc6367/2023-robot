from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

# this is one of your components
from subsystems.drivetrain import DriveTrain
from subsystems.grabber import Grabber
from subsystems.arm import Arm


class ScoringBase(AutonomousStateMachine):
    # Injected from the definition in robot.py
    drivetrain: DriveTrain
    grabber: Grabber
    arm: Arm

    @timed_state(first=True, duration=0.5, next_state="close_grabber")
    def open_grabber(self):
        self.grabber.release()

    @timed_state(duration=0.5, next_state="raise_to_level3")
    def close_grabber(self):
        self.grabber.grab()

    @state()
    def raise_to_level3(self):
        self.arm.gotoHi()
        if self.arm.getPosition() == "HI":
            self.next_state(self.move_forward)

    @timed_state(duration=1, next_state="release_grabber")
    def move_forward(self):
        self.drivetrain.move(0.2, 0)

    @timed_state(duration=1, next_state="back_up_out_the_community1")
    def release_grabber(self):
        self.grabber.release()

    @timed_state(duration=2, next_state="back_up_out_the_community2")
    def back_up_out_the_community1(self):
        self.drivetrain.move(-0.25, 0.07 * self.direction)

    @timed_state(duration=3, next_state="turning")
    def back_up_out_the_community2(self):
        self.arm.gotoOut()
        self.drivetrain.move(-0.3, -0.05 * self.direction)

    @timed_state(duration=3)
    def turning(self):
        self.drivetrain.move(0, 0.2 * self.direction)


class ScoringLeft(ScoringBase):
    MODE_NAME = "Scoring Left"
    DEFAULT = False

    def on_enable(self):
        self.direction = -1
        super().on_enable()


class ScoringRight(ScoringBase):
    MODE_NAME = "Scoring Right"
    DEFAULT = True

    def on_enable(self):
        self.direction = 1
        super().on_enable()
