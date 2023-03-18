import math
from wpimath.geometry import Pose2d, Rotation2d, Translation2d

# in meters
kTrackWidth = 0.6096

kWheelRadius = 0.1524 / 2
kPulsePerRevolution = 360
kDistancePerPulse = (2 * math.pi * kWheelRadius) / kPulsePerRevolution

# The max velocity and acceleration for our autonomous when using ramsete
kMaxSpeedMetersPerSecond = 1
kMaxAccelerationMetersPerSecondSquared = 0.75
kMaxVoltage = 10

kMaxCentripetalAcceleration = 1

# sysid filtered results from 2022 (git 172d5c42, window size=10)
kS_linear = 1.0898
kV_linear = 3.1382
kA_linear = 1.7421

kS_angular = 2.424
kV_angular = 3.3557
kA_angular = 1.461


class ArmConstants:
    kP = 0
    kSVolts = 0
    kGVolts = 0.17
    kVVoltSecondPerRad = 3.82
    kAVoltSecondSquaredPerRad = 0.02

    kMaxVelocityRadPerSecond = 3.5
    kMaxAccelerationRadPerSecSquared = 10

    # kEncoderPorts = (4, 5)
    # kEncoderPPR = 256
    # kEncoderDistancePerPulse = 2.0 * math.pi / kEncoderPPR

    # The offset of the arm from the horizontal in its neutral position,
    # measured from the horizontal
    kArmOffsetRads = 0.5


#
# Only used for simulation
#

# robot: 32.5 by 38

# Arm parameters in meters (approximate)
kArmLength = 1.1303  # 44.5 in
kArmMass = 4.5  # 10 lb
kArmGearing = 48  # actual is 208, but this feels better

rdeg = Rotation2d.fromDegrees
kStartingPose = Pose2d(2.881, 4.470, rdeg(-180))
