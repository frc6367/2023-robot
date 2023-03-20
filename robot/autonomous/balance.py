from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

from subsystems.drivetrain import DriveTrain
from components.auto_balance import AutoBalance


class AutoBalance(AutonomousStateMachine):
    # Injected from the definition in robot.py
    drivetrain: DriveTrain
    autobalance: AutoBalance

    @timed_state(first=True, duration=3)
    def auto(self):
        self.autobalance.autoBalanceRoutine()
