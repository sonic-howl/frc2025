import math

import rev
import wpilib
import wpimath.controller
import wpimath.geometry
import wpimath.kinematics
import wpimath.trajectory

import constants

kWheelRadius = 0.0508
kEncoderResolution = 4096
# rev neo is 42 for encoder resolutionz: try this out
kModuleMaxAngularVelocity = math.pi
kModuleMaxAngularAcceleration = math.tau

speeds = wpimath.kinematics.ChassisSpeeds(constants.vx, constants.vy, constants.omega)


class SwerveModule:
  def __init__(
    self, DriveMotorChannel: int, TurnMotorChannel: int, chassisAngularOffset: float
  ) -> None:
    """Constructs a SwerveModule with a Drive motor, Turn motor, Drive encoder and Turn encoder.

    :param DriveMotorChannel:      PWM output for the Drive motor.
    :param TurnMotorChannel:    PWM output for the Turn motor.
    """

    """ Initialize Spark Max motor controllers"""
    self.DriveSparkMax: rev.SparkBase = rev.SparkBase(
      DriveMotorChannel,
      rev.SparkBase.MotorType.kBrushless,
      rev._rev.SparkLowLevel.SparkModel.kSparkMax,
    )
    self.TurnSparkMax: rev.SparkBase = rev.SparkBase(
      TurnMotorChannel,
      rev.SparkBase.MotorType.kBrushless,
      rev._rev.SparkLowLevel.SparkModel.kSparkMax,
    )

    """ Initialize Spark Max encoders"""
    # Get Encoder Objects from Spark Max
    self.DriveEncoder: rev.SparkRelativeEncoder = self.DriveSparkMax.getEncoder(
      # rev.SparkMaxRelativeEncoder.Type.kHallSensor
    )
    self.TurnEncoder: rev.SparkAbsoluteEncoder = self.TurnSparkMax.getAbsoluteEncoder(
      # rev.SparkMaxAbsoluteEncoder.Type.kDutyCycle
    )

    """ Initialize PID Controllers"""
    # create spark max pid controllers
    self.DriveClosedLoopController = self.DriveSparkMax.getClosedLoopController()

    self.TurnClosedLoopController = self.TurnSparkMax.getClosedLoopController()

    # Swerve Drive parameters
    self.chassisAngularOffset = chassisAngularOffset
    self.desiredState = wpimath.kinematics.SwerveModuleState(
      0.0, wpimath.geometry.Rotation2d(self.TurnEncoder.getPosition())
    )
    self.DriveEncoder.setPosition(0)

  def getState(self) -> wpimath.kinematics.SwerveModuleState:
    """Returns the current state of the module.

    :returns: The current state of the module.
    """
    return wpimath.kinematics.SwerveModuleState(
      self.DriveEncoder.getVelocity(),
      wpimath.geometry.Rotation2d(
        self.TurnEncoder.getPosition() - self.chassisAngularOffset
      ),
    )

  def getPosition(self) -> wpimath.kinematics.SwerveModulePosition:
    """Returns the current position of the module.

    :returns: The current position of the module.
    """
    return wpimath.kinematics.SwerveModulePosition(
      self.DriveEncoder.getPosition(),
      wpimath.geometry.Rotation2d(
        self.TurnEncoder.getPosition() - self.chassisAngularOffset
      ),
    )

  def setDesiredState(self, desiredState: wpimath.kinematics.SwerveModuleState) -> None:
    """Sets the desired state for the module.

    :param desiredState: Desired state with speed and angle.
    """
    # Apply chassis angular offset to the desired state
    correctedDesiredState = wpimath.kinematics.SwerveModuleState(
      desiredState.speed,
      desiredState.angle + wpimath.geometry.Rotation2d(self.chassisAngularOffset),
    )

    TurnEncoderPosition = wpimath.geometry.Rotation2d(self.TurnEncoder.getPosition())
    # Optimize the reference state to avoid spinning further than 90 degrees
    correctedDesiredState.optimize(TurnEncoderPosition)

    # Command Drive and Turn SPARK MAX toward their respective setpoints
    self.DriveClosedLoopController.setReference(
      correctedDesiredState.speed, rev.SparkBase.ControlType.kVelocity
    )
    self.TurnClosedLoopController.setReference(
      correctedDesiredState.angle.radians(), rev.SparkBase.ControlType.kPosition
    )

    self.desiredState = desiredState

  def resetEncoders(self) -> None:
    self.DriveEncoder.setPosition(0)
