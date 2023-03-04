import magicbot
from subsystems.arm import Arm

from subsystems.grabber import Grabber


class AutoGrabber:
    grabber: Grabber
    arm: Arm

    enable = magicbot.tunable(True)
    activated = magicbot.will_reset_to(False)

    def activate(self):
        self.activated = True

    def execute(self):
        if (
            self.activated
            and self.enable
            and self.grabber.isObjectSensed()
            and self.arm.getPosition() in ("NEUTRAL", "OUT")
        ):
            self.grabber.grab()
