import math

import navx

# import networklogger
import ntcore
import wpilib
import wpimath.filter
import wpimath.geometry
import wpimath.kinematics
import wpimath.units

import constants
import swervemodule
import swerveutils


class DriveSubsystem:
  """
  Represents a swerve drive style drivetrain.
  """

  def __init__(self) -> None:
    self.kDriveKinematics = wpimath.kinematics.SwerveDrive4Kinematics(
      wpimath.geometry.Translation2d(
        constants.kWheelBase / 2, constants.kTrackWidth / 2
      ),
      wpimath.geometry.Translation2d(
        constants.kWheelBase / 2, -constants.kTrackWidth / 2
      ),
      wpimath.geometry.Translation2d(
        -constants.kWheelBase / 2, constants.kTrackWidth / 2
      ),
      wpimath.geometry.Translation2d(
        -constants.kWheelBase / 2, -constants.kTrackWidth / 2
      ),
    )

    self.frontLeft = swervemodule.SwerveModule(
      constants.kFrontLeftDriveMotorId,
      constants.kFrontLeftTurnMotorId,
      constants.kFrontLeftChassisAngularOffset,
    )
    self.backLeft = swervemodule.SwerveModule(
      constants.kBackLeftDriveMotorId,
      constants.kBackLeftTurnMotorId,
      constants.kBackLeftChassisAngularOffset,
    )
    self.frontRight = swervemodule.SwerveModule(
      constants.kFrontRightDriveMotorId,
      constants.kFrontRightTurnMotorId,
      constants.kFrontRightChassisAngularOffset,
    )
    self.backRight = swervemodule.SwerveModule(
      constants.kBackRightDriveMotorId,
      constants.kBackRightTurnMotorId,
      constants.kBackLeftChassisAngularOffset,
    )

    # the gyro sensor
    self.gyro = navx.AHRS(navx.AHRS.NavXComType.kMXP_SPI)

    # Slew rate filter variables for controlling the lateral acceleration
    self.currentRotation = 0.0
    self.currentTranslationDir = 0.0
    self.currentTranslationMag = 0.0

    self.magLimiter = wpimath.filter.SlewRateLimiter(constants.kMagnitudeSlewRate / 1)
    self.rotLimiter = wpimath.filter.SlewRateLimiter(constants.kRotationalSlewRate / 1)

    self.prevTime = ntcore._now() * pow(1, -6)  # secodns

    # Odometry class for tracking robot pose
    # 4 defines the number of modules
    self.odometry = wpimath.kinematics.SwerveDrive4Odometry(
      self.kDriveKinematics,
      # wpimath.geometry.Rotation2d(wpimath.units.degreesToRadians(self.gyro.getAngle())),
      self.gyro.getRotation2d(),
      (
        self.frontLeft.getPosition(),
        self.frontRight.getPosition(),
        self.backLeft.getPosition(),
        self.backRight.getPosition(),
      ),
      wpimath.geometry.Pose2d(),
    )

    self.resetEncoders()

    # logger object for sending data to smart dashboard
    # self.logger = networklogger.NetworkLogger()

  def periodic(self):
    self.odometry.update(
      # wpimath.geometry.Rotation2d(wpimath.units.degreesToRadians(self.gyro.getAngle())),
      self.gyro.getRotation2d(),
      (
        self.frontLeft.getPosition(),
        self.frontRight.getPosition(),
        self.backLeft.getPosition(),
        self.backRight.getPosition(),
      ),
    )

    # self.logger.log_gyro(self.gyro.getAngle())

  def drive(
    self,
    xSpeed: float,
    ySpeed: float,
    rot: float,
    fieldRelative: bool,
    rateLimit: bool,
  ) -> None:
    """
    Method to drive the robot using joystick info.
    :param xSpeed: Speed of the robot in the x direction (forward).
    :param ySpeed: Speed of the robot in the y direction (sideways).
    :param rot: Angular rate of the robot.
    :param fieldRelative: Whether the provided x and y speeds are relative to the field.
    :param rateLimit: Whether to enable rate limiting for smoother control
    :param periodSeconds: Time
    """
    xSpeedCommanded = None
    ySpeedCommanded = None

    if rateLimit:
      # Convert XY to polar for rate limiting
      inputTranslationDir = math.atan2(ySpeed, xSpeed)
      inputTranslationMag = math.sqrt(pow(xSpeed, 2) + pow(ySpeed, 2))

      # Calculate the direction slew rate based on an estimate of lateral acceleration
      directionSlewRate = None
      if self.currentTranslationMag != 0.0:
        directionSlewRate = abs(
          constants.kDirectionSlewRate / self.currentTranslationMag
        )
      else:
        directionSlewRate = 500.0  # some high number that means the slew rate is effectively instantaneous

      currentTime = ntcore._now() * pow(1, -6)
      elapsedTime = currentTime - self.prevTime
      angleDif = swerveutils.angleDifference(
        inputTranslationDir, self.currentTranslationDir
      )

      if angleDif < 0.45 * math.pi:
        self.currentTranslationDir = swerveutils.stepTowardsCircular(
          self.currentTranslationDir,
          inputTranslationDir,
          directionSlewRate * elapsedTime,
        )
        self.currentTranslationMag = self.magLimiter.calculate(inputTranslationMag)
      elif angleDif > 0.85 * math.pi:
        if self.currentTranslationMag > 1e-4:
          self.currentTranslationMag = self.magLimiter.calculate(0.0)
        else:
          self.currentTranslationDir = swerveutils.wrapAngle(
            self.currentTranslationDir + math.pi
          )
          self.currentTranslationMag = self.magLimiter.calculate(inputTranslationMag)
      else:
        self.currentTranslationDir = swerveutils.stepTowardsCircular(
          self.currentTranslationDir,
          inputTranslationDir,
          directionSlewRate * elapsedTime,
        )
        self.currentTranslationMag = self.magLimiter.calculate(0.0)

      self.prevTime = currentTime

      xSpeedCommanded = self.currentTranslationMag * math.cos(
        self.currentTranslationDir
      )
      ySpeedCommanded = self.currentTranslationMag * math.sin(
        self.currentTranslationDir
      )
      self.currentRotation = self.rotLimiter.calculate(rot)
    else:
      xSpeedCommanded = xSpeed
      ySpeedCommanded = ySpeed
      self.currentRotation = rot

    # Convert the commanded speeds into correct units for the drivetrain
    xSpeedDelivered = xSpeedCommanded * constants.kMaxSpeedMetersPerSecond
    ySpeedDelivered = ySpeedCommanded * constants.kMaxSpeedMetersPerSecond
    rotDelivered = self.currentRotation * constants.kMaxAngularSpeed

    (fl, fr, bl, br) = self.kDriveKinematics.toSwerveModuleStates(
      wpimath.kinematics.ChassisSpeeds.fromFieldRelativeSpeeds(
        xSpeedDelivered,
        ySpeedDelivered,
        rotDelivered,
        self.gyro.getRotation2d(),  # wpimath.geometry.Rotation2d(wpimath.units.degreesToRadians(self.gyro.getAngle()))
      )
      if fieldRelative
      else wpimath.kinematics.ChassisSpeeds(
        xSpeedDelivered, ySpeedDelivered, rotDelivered
      )
    )

    # Set the swerve modules to desired states
    self.setModuleStates((fl, fr, bl, br))

  def setX(self) -> None:
    self.frontLeft.setDesiredState(
      wpimath.kinematics.SwerveModuleState(
        0, wpimath.geometry.Rotation2d(wpimath.units.degreesToRadians(45))
      )
    )
    self.frontRight.setDesiredState(
      wpimath.kinematics.SwerveModuleState(
        0, wpimath.geometry.Rotation2d(wpimath.units.degreesToRadians(-45))
      )
    )
    self.backLeft.setDesiredState(
      wpimath.kinematics.SwerveModuleState(
        0, wpimath.geometry.Rotation2d(wpimath.units.degreesToRadians(-45))
      )
    )
    self.backRight.setDesiredState(
      wpimath.kinematics.SwerveModuleState(
        0, wpimath.geometry.Rotation2d(wpimath.units.degreesToRadians(45))
      )
    )

  def setModuleStates(
    self, desiredStates: tuple[wpimath.kinematics.SwerveModuleState]
  ) -> None:
    self.kDriveKinematics.desaturateWheelSpeeds(
      desiredStates, constants.kMaxSpeedMetersPerSecond
    )

    self.frontLeft.setDesiredState(desiredStates[0])
    self.frontRight.setDesiredState(desiredStates[1])
    self.backLeft.setDesiredState(desiredStates[2])
    self.backRight.setDesiredState(desiredStates[3])

  def resetEncoders(self) -> None:
    self.frontLeft.resetEncoders()
    self.backLeft.resetEncoders()
    self.frontRight.resetEncoders()
    self.backRight.resetEncoders()

  # Returns the robot's heading in degrees from -180 to 180
  def getHeading(self) -> float:
    return self.gyro.getRotation2d().degrees()
    # return wpimath.geometry.Rotation2d(wpimath.units.degreesToRadians(self.gyro.getAngle())).degrees()

  # Zeroes the heading of the robot
  def zeroHeading(self) -> None:
    self.gyro.reset()

  # Returns the turn rate of the robot in degrees per second
  def getTurnRate(self) -> float:
    return -self.gyro.getRate()

  # returns the currently-estimated pose
  def getPose(self) -> wpimath.geometry.Pose2d:
    return self.odometry.getPose()

  # Resets the odometry to the specified pose
  def resetOdometry(self, pose: wpimath.geometry.Pose2d):
    self.odometry.resetPosition(
      self.getHeading(),
      (
        self.frontLeft.getPosition(),
        self.frontRight.getPosition(),
        self.backLeft.getPosition(),
        self.backRight.getPosition(),
      ),
      pose,
    )
