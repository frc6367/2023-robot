import math

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

    do_autobalance1 = False
    do_autobalance2 = False

    # @timed_state(first=True, duration=0.25, next_state="close_grabber")
    # def open_grabber(self):
    #     self.grabber.release(force=True)

    # @timed_state(duration=0.5, next_state="wait")
    # def close_grabber(self):
    #     self.grabber.grab()

    # @timed_state(duration=0.5, next_state="raise_to_level3")
    # def wait(self):
    #     pass

    @timed_state(first=True, duration=3, next_state="move_forward")
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

    @timed_state(duration=0.5, next_state="initial_backup")
    def release_grabber(self):
        self.grabber.release()

    @timed_state(duration=2, next_state="back_up")
    def initial_backup(self):
        if self.do_autobalance2:
            self.next_state_now(self.start_new_autobalance)
        else:
            self.grabber.release()
            self.drivetrain.move(-0.25, 0.07 * self.direction)

    @state()
    def back_up(self):
        if self.do_autobalance1:
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
    # Autobalance (original)
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

    #
    # Autobalance (new technique)
    #

    debounce = 0

    def next_state_debounced(self, st, cnt=10):
        if self.debounce > cnt:
            self.debounce = 0
            self.next_state_now(st)
            return True
        else:
            self.debounce += 1
            return False

    @timed_state(duration=0.5, next_state="back_up_over_ramp")
    def start_new_autobalance(self, initial_call: bool):
        if initial_call:
            self.encoder_l.reset()

        self.grabber.release()
        # go over the ramp
        self.drivetrain.move(-0.3, 0)

    @state
    def back_up_over_ramp(self):
        self.arm.gotoNeutral()
        self.drivetrain.move(-0.3, 0)

        # exit when tilt is detected
        if self.autobalance.get_angle() > 12:
            self.next_state_debounced(self.ab_drive_up_ramp)

    @state
    def ab_drive_up_ramp(self):
        self.drivetrain.move(-0.2, 0)
        angle = self.autobalance.get_angle()
        if angle < 12:
            if self.next_state_debounced(self.equalize):
                print("equalize at", angle)

    @state
    def equalize(self):
        angle = self.autobalance.get_angle()

        # Note to self: I think these numbers are too small,
        # but probably we want a pid based overcome instead
        if angle > 8:
            self.autobalance.overcome(-0.1)
        elif angle > 5:
            self.autobalance.overcome(-0.05)
            self.debounce = 0
        elif angle < -8:
            self.autobalance.overcome(0.1)
            self.debounce = 0
        elif angle < -5:
            self.autobalance.overcome(0.05)
            self.debounce = 0
        else:
            self.autobalance.maintain()
            self.next_state_debounced(self.maintain, 25)

    # @timed_state(duration=0.5, next_state="back_up_over_ramp")
    # def start_new_autobalance(self, initial_call: bool):
    #     if initial_call:
    #         self.encoder_l.reset()

    #     self.grabber.release()
    #     # go over the ramp
    #     self.drivetrain.move(-0.45, 0)

    # @state
    # def back_up_over_ramp(self):
    #     self.arm.gotoNeutral()
    #     self.drivetrain.move(-0.35, 0)

    #     # hack
    #     if self.encoder_l.getDistance() > 3.25:
    #         self.next_state_now(self.come_back)

    # @state
    # def come_back(self):
    #     # come back over the ramp
    #     self.drivetrain.move(0.4, 0)

    #     if self.autobalance.get_angle() > 6:
    #         if self.debounce > 10:
    #             self.debounce = 0
    #             self.next_state_now(self.slow_on_charge_station)
    #         else:
    #             self.debounce += 1

    # @state
    # def slow_on_charge_station(self):
    #     # slow down on the ramp
    #     self.drivetrain.move(0.2, 0)

    #     if self.autobalance.get_angle() < 6:
    #         if self.debounce > 10:
    #             self.debounce = 0
    #             self.next_state_now(self.ensure_robot_is_flat)
    #         else:
    #             self.debounce += 1

    @state
    def ensure_robot_is_flat(self):
        # stop on the ramp
        angle = self.autobalance.get_angle()
        # if abs(angle) < 3.0:

        if angle > 8:
            self.drivetrain.move(-0.2, 0)
        elif angle < -8:
            self.drivetrain.move(0.2, 0)
        else:
            self.drivetrain.move(0, 0)


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


class ScoringHiAB_OG(ScoringBase):
    MODE_NAME = "Scoring HI Balance OG"
    DEFAULT = False
    do_autobalance1 = True

    def on_enable(self):
        self.direction = 0
        self.level = "MID"
        super().on_enable()


class ScoringMidAB_OG(ScoringBase):
    MODE_NAME = "Scoring MID Balance OG"
    DEFAULT = False
    do_autobalance1 = True

    def on_enable(self):
        self.direction = 0
        self.level = "MID2"
        super().on_enable()


class ScoringHiAB(ScoringBase):
    MODE_NAME = "Scoring HI Balance NEW"
    DEFAULT = False
    do_autobalance2 = True

    def on_enable(self):
        self.direction = 0
        self.level = "MID"
        super().on_enable()


class ScoringMidAB(ScoringBase):
    MODE_NAME = "Scoring MID Balance NEW"
    DEFAULT = False
    do_autobalance2 = True

    def on_enable(self):
        self.direction = 0
        self.level = "MID2"
        super().on_enable()
