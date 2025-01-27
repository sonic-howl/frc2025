import math

from wpimath import units
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics


class RobotConstants:
  # TODO: Measure the swerve module locations. (Units: Meters (m))
  #  Chassis configuration
  kTrackWidth = units.inchesToMeters(26.5)
  # Distance between centers of right and left wheels on robot
  kWheelBase = units.inchesToMeters(26.5)

  # Distance between front and back wheels on robot
  kDriveKinematics = SwerveDrive4Kinematics(
    Translation2d(kWheelBase / 2, kTrackWidth / 2),
    Translation2d(kWheelBase / 2, -kTrackWidth / 2),
    Translation2d(-kWheelBase / 2, kTrackWidth / 2),
    Translation2d(-kWheelBase / 2, -kTrackWidth / 2),
  )


class SwerveModuleConstants:
  kWheelRadius = None
  kEncoderResolution = None
  kModuleMaxAngularVelocity = math.pi
  kModuleMaxAngularAcceleration = math.tau


class DriveSubsystemConstants:
  kMaxSpeedMetersPerSecond = 4.8
  kMaxAngularSpeed = 2 * math.pi  # 1 rotation per second (in radians)

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


class ControllerConstants:
  kDriverControllerPort = 0
  kOperatorControllerPort = 1

  kDriveDeadband = 0.05
