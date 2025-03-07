import math

import navx
from commands2 import Subsystem
from ntcore import NetworkTableInstance
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.config import RobotConfig
from pathplannerlib.controller import PPHolonomicDriveController
from wpilib import DriverStation, SmartDashboard
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import (
  ChassisSpeeds,
  SwerveDrive4Kinematics,
  SwerveModuleState,
)

from config import Config
from constants import DriveSubsystemConstants, RobotConstants
from subsystems.SwerveModule import SwerveModule

from .vision import LimelightHelpers


class DriveSubsystem(Subsystem):
  fieldRelative = False

  def __init__(self):
    super().__init__()

    config = RobotConfig.fromGUISettings()

    self.frontLeft = SwerveModule(
      DriveSubsystemConstants.kFrontLeftDriveMotorId,
      DriveSubsystemConstants.kFrontLeftTurningMotorId,
      DriveSubsystemConstants.kFrontLeftChassisAngularOffset,
    )
    self.frontRight = SwerveModule(
      DriveSubsystemConstants.kFrontRightDriveMotorId,
      DriveSubsystemConstants.kFrontRightTurningMotorId,
      DriveSubsystemConstants.kFrontRightChassisAngularOffset,
    )
    self.backLeft = SwerveModule(
      DriveSubsystemConstants.kBackLeftDriveMotorId,
      DriveSubsystemConstants.kBackLeftTurningMotorId,
      DriveSubsystemConstants.kBackLeftChassisAngularOffset,
    )
    self.backRight = SwerveModule(
      DriveSubsystemConstants.kBackRightDriveMotorId,
      DriveSubsystemConstants.kBackRightTurningMotorId,
      DriveSubsystemConstants.kBackRightChassisAngularOffset,
    )

    self.gyro = navx.AHRS(navx.AHRS.NavXComType.kMXP_SPI)

    self.odometry = SwerveDrive4PoseEstimator(
      DriveSubsystemConstants.kDriveKinematics,
      self.gyro.getRotation2d(),
      (
        self.frontLeft.getPosition(),
        self.frontRight.getPosition(),
        self.backLeft.getPosition(),
        self.backRight.getPosition(),
      ),
      # Pose2d(7.585, 7, math.radians(-180)),
      Pose2d(),
    )

    # Configure the AutoBuilder last
    AutoBuilder.configure(
      self.getPose,
      self.resetOdometry,  # Method to reset odometry (will be called if your auto has a starting pose)
      self.getRobotRelativeSpeeds,  # ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
      lambda speeds, feedforwards: self.driveRobotRelative(
        speeds
      ),  # Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds. Also outputs individual module feedforwards
      PPHolonomicDriveController(  # PPHolonomicController is the built in path following controller for holonomic drive trains
        Config.DriveSubsystem.translationPPHolonominicDrivePID,  # Translation PID constants
        Config.DriveSubsystem.rotationPPHolonominicDrivePID,  # Rotation PID constants
      ),
      config,
      self.shouldFlipPath,
      self,
    )

    self.limelightHelpers = LimelightHelpers()

  def periodic(self) -> None:
    self.odometry.update(
      self.gyro.getRotation2d(),
      (
        self.frontLeft.getPosition(),
        self.frontRight.getPosition(),
        self.backLeft.getPosition(),
        self.backRight.getPosition(),
      ),
    )

    # get limelight megapose
    (pose, timestamp) = self.limelightHelpers.getLLPose()
    """
    https://github.com/LimelightVision/limelight-examples/blob/28cb4c8f9b68cea62bef010ab793960f8d2b7a53/java-wpilib/swerve-megatag-odometry/src/main/java/frc/robot/Drivetrain.java#L142
    """
    self.odometry.setVisionMeasurementStdDevs([0.7, 0.7, 9999999])
    self.odometry.addVisionMeasurement(pose, timestamp)

    self.updateShuffleBoard()

  def updateShuffleBoard(self):
    SmartDashboard.putNumber("FL Rot.", self.frontLeft.getPosition().angle.degrees())
    SmartDashboard.putNumber("FR Rot.", self.frontRight.getPosition().angle.degrees())
    SmartDashboard.putNumber("BL Rot.", self.backLeft.getPosition().angle.degrees())
    SmartDashboard.putNumber("BR Rot.", self.backRight.getPosition().angle.degrees())
    SmartDashboard.putNumber("Gryo", self.odometry.getEstimatedPosition().rotation().degrees())

  def getPose(self) -> Pose2d:
    """
    Returns the current pose of the robot.
    """
    return self.odometry.getEstimatedPosition()

  def resetOdometry(self, pose: Pose2d) -> None:
    """
    Resets the odometry to the specified pose.

    :param pose: THe pose to set the odometry to.
    """
    self.odometry.resetPosition(
      self.gyro.getRotation2d(),
      (
        self.frontLeft.getPosition(),
        self.frontRight.getPosition(),
        self.backLeft.getPosition(),
        self.backRight.getPosition(),
      ),
      pose,
    )

  def getHeading(self) -> float:
    """
    Returns the heading of the robot.

    :return the robot's heading in degrees, from -180 to 180
    """
    return self.gyro.getRotation2d()

  def getCurrentSpeeds(self) -> ChassisSpeeds:
    """
    Returns the current speeds of the robot.
    """
    return DriveSubsystemConstants.kDriveKinematics.toChassisSpeeds(
      (
        self.frontLeft.getState(),
        self.frontRight.getState(),
        self.backLeft.getState(),
        self.backRight.getState(),
      )
    )

  def getRobotRelativeSpeeds(self) -> ChassisSpeeds:
    """
    Returns the current speeds of the robot in robot relative coordinates.
    """
    return ChassisSpeeds.fromFieldRelativeSpeeds(
      self.getCurrentSpeeds().vx,
      self.getCurrentSpeeds().vy,
      self.getCurrentSpeeds().omega,
      self.gyro.getRotation2d(),
    )

  def setX(self):
    """
    Set the wheels in a X position (prevent movement)
    """
    self.frontLeft.setDesiredState(SwerveModuleState(0, Rotation2d.fromDegrees(45)))
    self.frontRight.setDesiredState(SwerveModuleState(0, Rotation2d.fromDegrees(-45)))
    self.backLeft.setDesiredState(SwerveModuleState(0, Rotation2d.fromDegrees(-45)))
    self.backRight.setDesiredState(SwerveModuleState(0, Rotation2d.fromDegrees(45)))

  def drive(self, xSpeed: float, ySpeed: float, rot: float, fieldRelative: bool) -> None:
    """
    Drives the robot using the specified x, y, and rotation speeds.

    :param xSpeed: The speed that the robot should drive in the X direction.
    :param ySpeed: The speed that the robot should drive in the Y direction.
    :param rot: The speed that the robot should rotate.
    :param fieldRelative: Whether the provided x and y speeds are relative to the field.
    """

    # Binds Joystick input values to robot max speeds
    xSpeedDelivered = xSpeed * DriveSubsystemConstants.kMaxSpeedMetersPerSecond
    ySpeedDelivered = ySpeed * DriveSubsystemConstants.kMaxSpeedMetersPerSecond
    rotDelivered = rot * DriveSubsystemConstants.kMaxAngularSpeed

    if fieldRelative:
      swerveModuleStates = DriveSubsystemConstants.kDriveKinematics.toSwerveModuleStates(
        ChassisSpeeds.fromFieldRelativeSpeeds(
          xSpeedDelivered, ySpeedDelivered, rotDelivered, self.gyro.getRotation2d()
        )
      )
    else:
      swerveModuleStates = DriveSubsystemConstants.kDriveKinematics.toSwerveModuleStates(
        ChassisSpeeds(xSpeedDelivered, ySpeedDelivered, rotDelivered)
      )

    states = SwerveDrive4Kinematics.desaturateWheelSpeeds(
      swerveModuleStates, DriveSubsystemConstants.kMaxSpeedMetersPerSecond
    )

    self.frontLeft.setDesiredState(states[0])
    self.frontRight.setDesiredState(states[1])
    self.backLeft.setDesiredState(states[2])
    self.backRight.setDesiredState(states[3])

  def driveRobotRelative(self, robotRelativeSpeeds: ChassisSpeeds) -> None:
    """
    Wrapper for PathPlanner to drive the robot in field relative coordinates.
    Drives the robot using the specified ChassisSpeeds.

    :param chassisSpeeds: The chassis speeds to drive the robot with.
    """
    targetSpeeds = ChassisSpeeds.discretize(robotRelativeSpeeds, 0.02)

    swerveModuleStates = DriveSubsystemConstants.kDriveKinematics.toSwerveModuleStates(targetSpeeds)

    states = SwerveDrive4Kinematics.desaturateWheelSpeeds(
      swerveModuleStates, DriveSubsystemConstants.kMaxSpeedMetersPerSecond
    )

    self.frontLeft.setDesiredState(states[0])
    self.frontRight.setDesiredState(states[1])
    self.backLeft.setDesiredState(states[2])
    self.backRight.setDesiredState(states[3])

  def shouldFlipPath(self):
    # Boolean supplier that controls when the path will be mirrored for the red alliance
    # This will flip the path being followed to the red side of the field.
    # THE ORIGIN WILL REMAIN ON THE BLUE SIDE
    return DriverStation.getAlliance() == DriverStation.Alliance.kRed

  def toggleFieldRelative(self):
    DriveSubsystem.fieldRelative = not DriveSubsystem.fieldRelative
