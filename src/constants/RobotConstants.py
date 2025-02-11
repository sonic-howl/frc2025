import math

from wpimath import units
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics

CONSTANTS_SHOULD_LOOK_LIKE_THIS = True


class RobotConstants:
  kFrameLength = units.inchesToMeters(30)
  kFrameWidth = units.inchesToMeters(26)


class ControllerConstants:
  kDriverControllerPort = 0
  kOperatorContollerPort = 1

  kDriveDeadband = 0.05


class DriveSubsystemConstants:
  kMaxSpeedMetersPerSecond = 4.8
  kMaxAngularSpeed = 2 * math.pi

  kDrirectionSlewRate = 1.2  # radians per second
  kMagnitudeSlewRate = 1.8  # percent per second (1 = 100%)
  kRotationalSlewRate = 2.0  # percent per second (1 = 100%)

  kFrontLeftTurningMotorId = 10
  kFrontLeftDriveMotorId = 11

  kFrontRightTurningMotorId = 12
  kFrontRightDriveMotorId = 13

  kBackLeftTurningMotorId = 14
  kBackLeftDriveMotorId = 15

  kBackRightTurningMotorId = 16
  kBackRightDriveMotorId = 17
