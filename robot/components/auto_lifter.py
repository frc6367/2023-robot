import magicbot
from subsystems.arm import Arm

from subsystems.grabber import Grabber


class AutoLifter:
    grabber: Grabber
    arm: Arm

    enable = magicbot.tunable(True)
    activated = magicbot.will_reset_to(False)

    acted = False

    def activate(self):
        self.activated = True

    def execute(self):
        if (
            self.activated
            and self.enable
            and self.grabber.isObjectSensed()
            and self.arm.getAngleRad() < self.arm.LOW_MAX
        ):
            if not self.acted:
                self.arm.gotoLow()
                self.acted = True
        else:
            if not self.grabber.isObjectSensed():
                self.acted = False
