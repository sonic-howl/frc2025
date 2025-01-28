import math

from wpimath import units
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics


class RobotConstants:
  kFrameLength = units.inchesToMeters(30)
  kFrameWidth = units.inchesToMeters(26)


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
  # Use WPILib Coordinate System Conventions to Calculate: https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html
  kFrontLeftChassisAngularOffset = math.tan(
    (RobotConstants.kFrameLength / 2) / (RobotConstants.kFrameWidth / 2)
  )
  kFrontRightChassisAngularOffset = kFrontLeftChassisAngularOffset - math.pi
  kBackLeftChassisAngularOffset = kFrontLeftChassisAngularOffset + math.pi
  kBackRightChassisAngularOffset = kFrontLeftChassisAngularOffset - (2 * math.pi)


class SwerveModuleConstants:
  kWheelDiameter = units.inchesToMeters(3)
  kWheelCircumference = kWheelDiameter * math.pi
  kDriveMotorGearRatio = 1 / 4.71

  @staticmethod
  def driveMotorRotationsToMeters(rotations: float) -> float:
    """
    Convert the drive motor's encoder readings from rotations to meters
    Will work for rotations or rotations per minute

    :param rpm: Rotations or Rotations per Minute
    """
    rps = rotations / 60

    return (
      SwerveModuleConstants.kWheelCircumference
      * rps
      * SwerveModuleConstants.kDriveMotorGearRatio
    )

  @staticmethod
  def driveMotorMetersPerSecondToDriveMotorRotationsPerSecond(
    metersPerSecond: float,
  ) -> float:
    """
    Convert speed in meters per second to wheel rotations per second.

    :param metersPerSecond: Speed in meters per second
    :return: Speed in wheel rotations per second
    """
    return metersPerSecond / SwerveModuleConstants.kWheelCircumference
