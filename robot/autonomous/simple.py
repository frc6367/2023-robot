from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

# this is one of your components
from subsystems.drivetrain import DriveTrain
from subsystems.grabber import Grabber
from subsystems.arm import Arm


class scoring(AutonomousStateMachine):
    MODE_NAME = "scoring"
    DEFAULT = False

    # Injected from the definition in robot.py
    drivetrain: DriveTrain
    grabber: Grabber
    arm: Arm

    @state(first=True)
    def raise_to_level3(self):
        self.arm.gotoHi()
        if self.arm.getPosition() == "HI":
            self.next_state(self.move_forward)

    @timed_state(duration=1, next_state="release_grabber")
    def move_forward(self):
        self.drivetrain.move(0.2, 0)

        # self.drivetrain.move_encoder_stright(20)

        # if self.drivetrain.is_at_desired_position():
        #     self.next_state(self.release_grabber)

    @timed_state(duration=1, next_state="back_up_out_the_communtiy")
    def release_grabber(self):
        self.grabber.release()

    @timed_state(duration=3)
    def back_up_out_the_communtiy(self):
        self.drivetrain.move(-0.2, 0)
        # self.drivetrain.move_encoder_backwards(-20)

        # if self.drivetrain.is_at_desired_position():
        #     breakpoint
