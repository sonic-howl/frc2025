import math

from wpimath import units
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics


class RobotConstants:
  # TODO: Measure the swerve module lcoations: (Units: Meters (m))
  kFrameLength = units.inchesToMeters(26.5)
  kFrameWidth = units.inchesToMeters(26.5)


class ControllerConstants:
  kDriverControllerPort = 0
  kOperatorControllerPort = 1

  kDriveDeadband = 0.05


class DriveSubsystemConstants:
  kMaxSpeedMetersPerSecond = 4.8
  kMaxAngularSpeed = 2 * math.pi  # 1 rotation per second (in radians)

  # WPILib Coordinate System Conventions: https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html
  kDriveKinematics = SwerveDrive4Kinematics(
    Translation2d(RobotConstants.kFrameWidth / 2, RobotConstants.kFrameLength / 2),
    Translation2d(RobotConstants.kFrameWidth / 2, -RobotConstants.kFrameLength / 2),
    Translation2d(-RobotConstants.kFrameWidth / 2, RobotConstants.kFrameLength / 2),
    Translation2d(-RobotConstants.kFrameWidth / 2, -RobotConstants.kFrameLength / 2),
  )
  ### Motor Ids ### (Turning: Even, Drive: Odd) [Ids: 10-19 (18,19 are extra)]
  kFrontLeftTurningMotorId = 10
  kFrontLeftDriveMotorId = 11

  kFrontRightTurningMotorId = 12
  kFrontRightDriveMotorId = 13

  kBackLeftTurningMotorId = 14
  kBackLeftDriveMotorId = 15

  kBackRightTurningMotorId = 16
  kBackRightDriveMotorId = 17

  ### Angular Offsets ### (in radians)
  # TODO: Measure the angular offsets of the swerve modules.
  kFrontLeftChassisAngularOffset = -math.pi / 2
  kFrontRightChassisAngularOffset = 0
  kBackLeftChassisAngularOffset = math.pi
  kBackRightChassisAngularOffset = math.pi / 2
