import math

# in meters
kTrackWidth = 0.6096

kWheelRadius = 0.1524 / 2
kPulsePerRevolution = 360
kDistancePerPulse = (2 * math.pi * kWheelRadius) / kPulsePerRevolution
