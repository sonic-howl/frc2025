import math

import wpimath.geometry


class RobotConstants:
  # TODO: Measure the swerve module locations. (Units: Meters (m))
  kFrontLeftLocation = wpimath.geometry.Translation2d(0.381, 0.381)
  kFrontRightLocation = wpimath.geometry.Translation2d(0.381, -0.381)
  kBackLeftLocation = wpimath.geometry.Translation2d(-0.381, 0.381)
  kBackRightLocation = wpimath.geometry.Translation2d(-0.381, -0.381)


class SwerveModuleConstants:
  kWheelRadius = None
  kEncoderResolution = None
  kModuleMaxAngularVelocity = math.pi
  kModuleMaxAngularAcceleration = math.tau


class DriveSubsystemConstants:
  kMaxSpeed = 3.0  # m/s
  kMaxAngularSpeed = math.pi  # 1/2 rotation per second

  # Motor Ids (Turning: Even, Drive: Odd) [Ids: 10-19 (18,19 are extra)]
  kFrontLeftTurningMotorId = 10
  kFrontLeftDriveMotorId = 11

  kFrontRightTurningMotorId = 12
  kFrontRightDriveMotorId = 13

  kBackLeftTurningMotorId = 14
  kBackLeftDriveMotorId = 15

  kBackRightTurningMotorId = 16
  kBackRightDriveMotorId = 17

  # Encoder Ids
  kFrontLeftDriveEncoderAId = 0
  kFrontLeftDriveEncoderBId = 1
  kFrontLeftTurningEncoderAId = 2
  kFrontLeftTurningEncoderBId = 3

  kFrontRightDriveEncoderAId = 4
  kFrontRightDriveEncoderBId = 5
  kFrontRightTurningEncoderAId = 6
  kFrontRightTurningEncoderBId = 7

  kBackLeftDriveEncoderAId = 8
  kBackLeftDriveEncoderBId = 9
  kBackLeftTurningEncoderAId = 10
  kBackLeftTurningEncoderBId = 11

  kBackRightDriveEncoderAId = 12
  kBackRightDriveEncoderBId = 13
  kBackRightTurningEncoderAId = 14
  kBackRightTurningEncoderBId = 15


class ControllerConstants:
  kDriverControllerPort = 0
  kOperatorControllerPort = 1
