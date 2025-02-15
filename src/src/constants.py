import math

import rev
from wpimath import units
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics

### Robot Constants
kFrameLength = units.inchesToMeters(30)
kFrameWidth = units.inchesToMeters(26)

kWheelCenterOffset = units.inchesToMeters(1.5)

kWheelBase = kFrameLength - 2 * kWheelCenterOffset  # METERS
kTrackWidth = kFrameWidth - 2 * kWheelCenterOffset  # METERS


### Controller Constants
kDriverControllerPort = 0
kOperatorContollerPort = 1

kDriveDeadband = 0.05

### Drive Subsystem Constants
kMaxSpeedMetersPerSecond = 4.8
kMaxAngularSpeed = 2 * math.pi

kDrirectionSlewRate = 1.2  # radians per second
kMagnitudeSlewRate = 1.8  # percent per second (1 = 100%)
kRotationalSlewRate = 2.0  # percent per second (1 = 100%)

kFrontLeftChassisAngularOffset = -math.pi / 2
kFrontRightChassisAngularOffset = 0
kBackLeftChassisAngularOffset = math.pi
kBackRightChassisAngularOffset = math.pi / 2

kFrontLeftTurnMotorId = 10
kFrontLeftDriveMotorId = 11

kFrontRightTurnMotorId = 12
kFrontRightDriveMotorId = 13

kBackLeftTurnMotorId = 14
kBackLeftDriveMotorId = 15

kBackRightTurnMotorId = 16
kBackRightDriveMotorId = 17


### Swerve Module Constants
# Invert the Turn encoder, since the output shaft rotates in the opposite direction
# of the steering motor in the MAXSwerve Module
kTurnEncoderInverted = True

kDriveMotorPinionTeeth = 14
kWheelDiameter = units.inchesToMeters(3)

kDriveMotorFreeSpeedRps = 5676 / 60

kWheelCircumference = kWheelDiameter * math.pi
# 45 teeth on bevel gear, 22 on first-stage spur gear, 15 on bevel pinion
kDriveMotorReduction = (45.0 * 22) / (kDriveMotorPinionTeeth * 15)
kDriveWheelFreeSpeedRps = (
  kDriveMotorFreeSpeedRps * kWheelCircumference
) / kDriveMotorReduction
kDriveEncoderPositionFactor = (
  kWheelDiameter * math.pi
) / kDriveMotorReduction  # Meters
kDriveEncoderVelocityFactor = (
  (kWheelDiameter * math.pi) / kDriveMotorReduction
) / 60.0  # Meters per second

kTurnEncoderPositionFactor = 2 * math.pi  # radians
kTurnEncoderVelocityFactor = (2 * math.pi) / 60.0  # meters per second

kTurnEncoderPositionPIDMinInput = 0
kTurnEncoderPositionPIDMaxInput = kTurnEncoderPositionFactor

# Closed Loop (PID) Constants
kDriveP = 0
kDriveI = 0
kDriveD = 0
kDriveFF = 1 / kDriveWheelFreeSpeedRps
kDriveMinOutput = -1
kDriveMaxOutput = 1

kTurnP = 1
kTurnI = 0
kTurnD = 0
kTurnFF = 0
kTurnMinOutput = -1
kTurnMaxOutput = 1

kDriveMotorIdleMode: rev.SparkBaseConfig.IdleMode = (
  rev._rev.SparkBaseConfig().IdleMode.kCoast
)
kTurnMotorIdleMode: rev.SparkBaseConfig.IdleMode = (
  rev._rev.SparkBaseConfig().IdleMode.kCoast
)
