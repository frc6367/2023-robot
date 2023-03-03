import math

# in meters
kTrackWidth = 0.6096

kWheelRadius = 0.1524 / 2
kPulsePerRevolution = 360
kDistancePerPulse = (2 * math.pi * kWheelRadius) / kPulsePerRevolution

#
# Only used for simulation
#

# Arm parameters in meters (approximate)
kArmLength = 1.1303 # 44.5 in
kArmMass = 4.5  # 10 lb
kArmGearing = 48 # actual is 208, but this feels better

