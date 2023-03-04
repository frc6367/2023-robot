import dataclasses
import enum
import typing

import magicbot
import wpilib

from wpimath.geometry import Pose2d, Rotation2d, Transform2d
from wpimath.trajectory import TrajectoryGenerator, Trajectory

from subsystems.grabber import Grabber
from subsystems.arm import Arm
from subsystems.drivetrain import DriveTrain

from components.ramsete import RamseteComponent

rdeg = Rotation2d.fromDegrees


class AType(enum.Enum):
    # Each action must specify one of the following
    TRAJECTORY = 1
    WAIT_FOR_ARM = 2

    GRAB = 3
    RELEASE = 4

    SLOW_FWD = 5


@dataclasses.dataclass
class Action:
    type: AType
    arm_pos: str
    waypoints: typing.Optional[typing.List[Pose2d]] = None
    reverse: bool = False

    # Generated by the constructor
    traj: typing.Optional[Trajectory] = None


class ComplexBase(magicbot.AutonomousStateMachine):
    # All actions
    # actions: typing.List[Action]

    # Current action
    # action: typing.Optional[Action]

    # Components
    arm: Arm
    grabber: Grabber
    ramsete: RamseteComponent
    drivetrain: DriveTrain

    def setup(self):
        self.setup_actions()
        self.idx = -1
        self.action = None

        trajectory = Trajectory()

        last_waypoint = None
        for action in self.actions:
            if not action.waypoints:
                continue

            if last_waypoint:
                waypoints = [last_waypoint] + action.waypoints
            else:
                waypoints = action.waypoints

            last_waypoint = waypoints[-1]

            if action.reverse:
                cfg = self.ramsete.tconfig_rev
            else:
                cfg = self.ramsete.tconfig

            action.traj = TrajectoryGenerator.generateTrajectory(waypoints, cfg)
            trajectory += action.traj

        self.ramsete.register_autonomous_trajectory(self.MODE_NAME, trajectory)

    def on_enable(self):
        super().on_enable()
        self.idx = 0

    @magicbot.state(first=True)
    def begin_action(self):
        self.idx += 1
        if len(self.actions) == self.idx:
            self.done()
            return

        self.action = action = self.actions[self.idx]
        self.logger.info("Begin action %d", self.idx)

        # Always specifies an arm position
        if action.arm_pos == "HI":
            self.arm.gotoHi()
        elif action.arm_pos == "OUT":
            self.arm.gotoOut()
        elif action.arm_pos == "MID":
            self.arm.gotoMiddle()
        elif action.arm_pos == "LOW":
            self.arm.gotoLow()
        elif action.arm_pos == "NEUTRAL":
            self.arm.gotoNeutral()
        else:
            assert False

        if self.action.type == AType.RELEASE:
            self.next_state_now(self.grabber_release)
        elif self.action.type == AType.TRAJECTORY:
            self.tstate = self.ramsete.startTrajectory(action.traj)
            self.next_state_now(self.trajectory_drive)
        elif self.action.type == AType.WAIT_FOR_ARM:
            self.next_state_now(self.wait_for_arm)
        elif self.action.type == AType.GRAB:
            self.next_state_now(self.grabber_grab)
        elif self.action.type == AType.SLOW_FWD:
            self.next_state_now(self.slow_fwd)
        else:
            assert False

    @magicbot.timed_state(duration=0.5, next_state="begin_action")
    def grabber_grab(self):
        self.grabber.grab()

    @magicbot.timed_state(duration=0.5, next_state="begin_action")
    def grabber_release(self):
        self.grabber.release()

    @magicbot.state()
    def trajectory_drive(self):
        if self.tstate.done:
            self.next_state_now(self.begin_action)
            return

    @magicbot.timed_state(duration=1, next_state="begin_action")
    def slow_fwd(self):
        self.drivetrain.move(0.2, 0)

    @magicbot.state()
    def wait_for_arm(self):
        if self.arm.getPosition() == self.action.arm_pos:
            self.next_state_now(self.begin_action)


# 2ft in meters
TWO_FEET = 0.6096


class FwdBkwdBase(ComplexBase):
    def setup_actions(self):
        self.actions = [
            # Release
            Action(AType.RELEASE, "NEUTRAL"),
            # Grab
            Action(AType.GRAB, "NEUTRAL"),
            # raise to level 3
            Action(AType.WAIT_FOR_ARM, "HI"),
            # move forward slightly without using encoders
            # - this is because we're pushing against the wall so
            #   the encoder stuff will get messed up
            Action(AType.SLOW_FWD, "HI"),
            # Action(
            #     AType.TRAJECTORY,
            #     "HI",
            #     waypoints=[
            #         Pose2d(0, 0, rdeg(0)),
            #         Pose2d(TWO_FEET, 0, rdeg(0)),
            #     ],
            # ),
            # Release the grabber
            Action(AType.RELEASE, "HI", waypoints=[]),
            # Back up while keeping the arm out
            Action(
                AType.TRAJECTORY,
                "HI",
                waypoints=[
                    Pose2d(TWO_FEET, 0, rdeg(0)),
                    Pose2d(0, self.OFFSET, rdeg(0)),
                    Pose2d(-3, self.OFFSET, rdeg(0)),
                ],
                reverse=True,
            ),
            Action(AType.WAIT_FOR_ARM, "OUT"),
            # Back up and bring the arm to zero
            # Action(
            #     AType.TRAJECTORY,
            #     "OUT",
            #     waypoints=[
            #         Pose2d(0, self.OFFSET, rdeg(0)),
            #         Pose2d(-3, self.OFFSET, rdeg(0)),
            #     ],
            #     reverse=True,
            # ),
        ]


class FwdBkwdLeft(FwdBkwdBase):
    MODE_NAME = "FwdBack Left"
    DEFAULT = False
    OFFSET = 0.2


class FwdBkwdRight(FwdBkwdBase):
    MODE_NAME = "FwdBack Right"
    DEFAULT = False
    OFFSET = -0.2
