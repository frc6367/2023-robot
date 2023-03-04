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

#
# Only used for simulation
#

# Arm parameters in meters (approximate)
kArmLength = 1.1303  # 44.5 in
kArmMass = 4.5  # 10 lb
kArmGearing = 48  # actual is 208, but this feels better

rdeg = Rotation2d.fromDegrees
kStartingPose = Pose2d(2.881, 4.470, rdeg(-180))
