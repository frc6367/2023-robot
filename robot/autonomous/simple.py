from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

# this is one of your components
from subsystems.drivetrain import DriveTrain
from subsystems.grabber import Grabber
from subsystems.arm import Arm

from components.auto_balance import AutoBalance


class ScoringBase(AutonomousStateMachine):
    # Injected from the definition in robot.py
    drivetrain: DriveTrain
    grabber: Grabber
    arm: Arm
    autobalance: AutoBalance

    encoder_l: wpilib.Encoder
    encoder_r: wpilib.Encoder

    do_autobalance = False

    @timed_state(first=True, duration=0.25, next_state="close_grabber")
    def open_grabber(self):
        self.grabber.release(force=True)

    @timed_state(duration=0.5, next_state="wait")
    def close_grabber(self):
        self.grabber.grab()

    @timed_state(duration=0.5, next_state="raise_to_level3")
    def wait(self):
        pass

    @timed_state(duration=3, next_state="move_forward")
    def raise_to_level3(self):
        if self.level == "MID":
            self.arm.gotoMiddle()
        else:
            self.arm.gotoMiddle2()
        if self.arm.getPosition() == self.level:
            self.next_state(self.move_forward)

    @timed_state(duration=1.1, next_state="release_grabber")
    def move_forward(self):
        if self.level == "MID2":
            self.next_state_now(self.move_forward_less)
            return

        self.drivetrain.move(0.2, 0)

    @timed_state(duration=0.6, next_state="release_grabber")
    def move_forward_less(self):
        self.drivetrain.move(0.2, 0)

    @timed_state(duration=1, next_state="initial_backup")
    def release_grabber(self):
        self.grabber.release()

    @timed_state(duration=2, next_state="back_up")
    def initial_backup(self):
        self.drivetrain.move(-0.25, 0.07 * self.direction)

    @state()
    def back_up(self):
        if self.do_autobalance:
            self.next_state_now(self.wait_for_autobalance)
        else:
            self.next_state_now(self.back_up_out_the_community)

    #
    # Community + turning
    #

    @timed_state(duration=3, next_state="turning")
    def back_up_out_the_community(self):
        self.arm.gotoOut()
        self.drivetrain.move(-0.3, -0.05 * self.direction)

    @timed_state(duration=3)
    def turning(self):
        self.drivetrain.move(0, 0.2 * self.direction)

    #
    # Autobalance
    #

    @timed_state(duration=2, next_state="ramp_up")
    def wait_for_autobalance(self):
        self.arm.gotoNeutral()

    @timed_state(duration=6)
    def ramp_up(self, initial_call: bool):
        if initial_call:
            self.encoder_l.reset()

        self.drivetrain.move(-0.4, 0)

        # hack
        if self.encoder_l.getDistance() > 1.35:
            self.next_state_now(self.maintain)

    @state()
    def maintain(self):
        self.autobalance.maintain()


class ScoringLeft(ScoringBase):
    MODE_NAME = "Scoring HI Left"
    DEFAULT = False

    def on_enable(self):
        self.direction = -1
        self.level = "MID"
        super().on_enable()


class ScoringRight(ScoringBase):
    MODE_NAME = "Scoring HI Right"
    DEFAULT = True

    def on_enable(self):
        self.direction = 1
        self.level = "MID"
        super().on_enable()


class ScoringMidLeft(ScoringBase):
    MODE_NAME = "Scoring MID Left"
    DEFAULT = False

    def on_enable(self):
        self.direction = -1
        self.level = "MID2"
        super().on_enable()


class ScoringMidRight(ScoringBase):
    MODE_NAME = "Scoring MID Right"
    DEFAULT = False

    def on_enable(self):
        self.direction = 1
        self.level = "MID2"
        super().on_enable()


class ScoringHiAB(ScoringBase):
    MODE_NAME = "Scoring HI Balance"
    DEFAULT = False
    do_autobalance = True

    def on_enable(self):
        self.direction = 0
        self.level = "MID"
        super().on_enable()


class ScoringMidAB(ScoringBase):
    MODE_NAME = "Scoring MID Balance"
    DEFAULT = False
    do_autobalance = True

    def on_enable(self):
        self.direction = 0
        self.level = "MID2"
        super().on_enable()
