import math

from wpimath import units
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics


class RobotConstants:
  kFrameLength = units.inchesToMeters(30)
  kFrameWidth = units.inchesToMeters(26)

  kWheelCenterOffset = units.inchesToMeters(1.5)


class DriverControllerConstants:
  kDriverControllerPort = 0

  kDriveDeadband = 0.05


class OperatorControllerConstants:
  kOperatorControllerPort = 1

  kElevateDeadband = 0.05


class DriveSubsystemConstants:
  kMaxSpeedMetersPerSecond = 4.8
  kMaxAngularSpeed = math.pi * 2  # 1 rotation per second (in radians)

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
  ### Motor Ids ### (Turning: Even, Drive: Odd) [Ids: 9-19 (17, 18, 19 are extra)]
  # Temporarily changed to ROBOT POV
  # Should be undone, and updated in config.py for more consistency
  kFrontLeftTurningMotorId = 10
  kFrontLeftDriveMotorId = 9

  kFrontRightTurningMotorId = 12
  kFrontRightDriveMotorId = 11

  kBackLeftTurningMotorId = 14
  kBackLeftDriveMotorId = 13

  kBackRightTurningMotorId = 16
  kBackRightDriveMotorId = 15

  ### Angular Offsets ### (in radians)
  kFrontLeftChassisAngularOffset = -math.pi / 2
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
  kWheelFreeSpeedRotationsPerSecond = kDrivingMotorFreeSpeedRotationsPerSecond * kWheelCircumference / kDriveMotorReduction

  kDriveMotorGearRatio = 1 / kDriveMotorReduction


class ElevatorSubsystemConstants:
  kManualElevatorSpeed = 0.5

  kLeftElevatorMotorId = 20
  kRightElevatorMotorId = 21


class PickupSubsystemConstants:
  kPickupSpeed = 0.5

  kUpperPickupMotorId = 22
  kLowerPickupMotorId = 23
