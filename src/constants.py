import math

from wpimath import units
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics


class RobotConstants:
  # Used with: https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html
  x = units.inchesToMeters(28)
  y = units.inchesToMeters(30)

  kWheelCenterOffset = units.inchesToMeters(2)


class DriverControllerConstants:
  kDriverControllerPort = 0

  kDriveDeadband = 0.05


class OperatorControllerConstants:
  kOperatorControllerPort = 1

  kElevateDeadband = 0.05
  kPickupDeadband = 0.05


class DriveSubsystemConstants:
  kMaxSpeedMetersPerSecond = 4  # TODO
  kMaxAngularSpeed = math.radians(720)  # radians per second

  # WPILib Coordinate System Conventions: https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html
  kDriveKinematics = SwerveDrive4Kinematics(
    Translation2d(
      (RobotConstants.x / 2) - RobotConstants.kWheelCenterOffset,
      (RobotConstants.y / 2) - RobotConstants.kWheelCenterOffset,
    ),
    Translation2d(
      (RobotConstants.x / 2) - RobotConstants.kWheelCenterOffset,
      -((RobotConstants.y / 2) - RobotConstants.kWheelCenterOffset),
    ),
    Translation2d(
      -((RobotConstants.x / 2) - RobotConstants.kWheelCenterOffset),
      (RobotConstants.y / 2) - RobotConstants.kWheelCenterOffset,
    ),
    Translation2d(
      -((RobotConstants.x / 2) - RobotConstants.kWheelCenterOffset),
      -((RobotConstants.y / 2) - RobotConstants.kWheelCenterOffset),
    ),
  )

  ### Motor Ids ### (Turning: Even, Drive: Odd) [Ids: 10-19 (18,19 are extra)]
  # Follows the WPILib Coordinate System Conventions: https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html
  kFrontLeftTurningMotorId = 12
  kFrontLeftDriveMotorId = 11

  kFrontRightTurningMotorId = 10
  kFrontRightDriveMotorId = 9

  kBackLeftTurningMotorId = 16
  kBackLeftDriveMotorId = 15

  kBackRightTurningMotorId = 14
  kBackRightDriveMotorId = 13

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
  kWheelFreeSpeedRotationsPerSecond = (
    kDrivingMotorFreeSpeedRotationsPerSecond * kWheelCircumference / kDriveMotorReduction
  )

  kDriveMotorGearRatio = 1 / kDriveMotorReduction

  squareInputs = True


class ElevatorSubsystemConstants:
  kManualElevatorSpeed = 0.75

  kS = 0
  kG = 0.3
  kV = 3
  kA = 0

  kP = 0.35
  kI = 0
  kD = 0
  kClosedLoopSlot = 0

  kMotorForwardSoftLimit = 0.88
  kMotorReverseSoftLimit = 0

  kMotorMaxVelocity = 1.5
  kMotorAcceleration = 4

  kMiddleSetPoint = 0.86
  kBottomSetPoint = 0.5
  kScoreSetPoint = 0.28

  kLeftElevatorMotorId = 20
  kRightElevatorMotorId = 21

  kUpperSwitchChannel = 0
  kLowerSwitchChannel = 1


class PickupSubsystemConstants:
  kManualPickupSpeed = 0.5

  kUpperPickupMotorId = 22
  kLowerPickupMotorId = 23
