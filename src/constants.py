import math

from wpimath import units
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics


class RobotConstants:
  kFrameLength = units.inchesToMeters(30)
  kFrameWidth = units.inchesToMeters(26)

  kWheelCenterOffset = units.inchesToMeters(1.5)


class ControllerConstants:
  kDriverControllerPort = 0
  kOperatorControllerPort = 1

  kDriveDeadband = 0.05


class DriveSubsystemConstants:
  kMaxSpeedMetersPerSecond = 4.8
  kMaxAngularSpeed = 2 * math.pi  # 1 rotation per second (in radians)

  # WPILib Coordinate System Conventions: https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html
  kDriveKinematics = SwerveDrive4Kinematics(
    Translation2d(
      (RobotConstants.kFrameWidth / 2) - RobotConstants.kWheelCenterOffset,
      (RobotConstants.kFrameLength / 2) - RobotConstants.kWheelCenterOffset,
    ),
    Translation2d(
      (RobotConstants.kFrameWidth / 2) - RobotConstants.kWheelCenterOffset,
      (-RobotConstants.kFrameLength / 2) - RobotConstants.kWheelCenterOffset,
    ),
    Translation2d(
      (-RobotConstants.kFrameWidth / 2) - RobotConstants.kWheelCenterOffset,
      (RobotConstants.kFrameLength / 2) - RobotConstants.kWheelCenterOffset,
    ),
    Translation2d(
      (-RobotConstants.kFrameWidth / 2) - RobotConstants.kWheelCenterOffset,
      (-RobotConstants.kFrameLength / 2) - RobotConstants.kWheelCenterOffset,
    ),
  )
  ### Motor Ids ### (Turning: Even, Drive: Odd) [Ids: 10-19 (18,19 are extra)]
  # Temporarily changed to ROBOT POV
  # Should be undone, and updated in config.py for more consistency
  kFrontLeftTurningMotorId = 12
  kFrontLeftDriveMotorId = 13

  kFrontRightTurningMotorId = 10
  kFrontRightDriveMotorId = 11

  kBackLeftTurningMotorId = 16
  kBackLeftDriveMotorId = 17

  kBackRightTurningMotorId = 14
  kBackRightDriveMotorId = 15

  ### Angular Offsets ### (in radians)
  # Use WPILib Coordinate System Conventions to Calculate: https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html
  kFrontLeftChassisAngularOffset = math.pi / 2
  kFrontRightChassisAngularOffset = 0
  kBackLeftChassisAngularOffset = math.pi
  kBackRightChassisAngularOffset = math.pi / 2


class SwerveModuleConstants:
  """
  Translated from java, based on https://github.com/REVrobotics/MAXSwerve-Java-Template/blob/main/src/main/java/frc/robot/Constants.java

  The MAXSwerve module can be configured with one of three pinion gears: 12T,
  13T, or 14T. This changes the drive speed of the module (a pinion gear with
  more teeth will result in a robot that drives faster).
  """

  kDriveMotorPinionTeeth = 14

  kWheelDiameter = units.inchesToMeters(3)
  kWheelCircumference = kWheelDiameter * math.pi
  kDrivingMotorFreeSpeedRotationsPerSecond = 5676 / 60
  # 45 teeth on bevel gear, 22 on first-stage spur gear, 15 on bevel pinion
  kDriveMotorReduction = (45.0 * 22) / (kDriveMotorPinionTeeth * 15)
  kWheelFreeSpeedRotationsPerSecond = (
    kDrivingMotorFreeSpeedRotationsPerSecond
    * kWheelCircumference
    / kDriveMotorReduction
  )

  kDriveMotorGearRatio = 1 / kDriveMotorReduction

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
