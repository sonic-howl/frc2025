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
      DriveMotorChannel, rev.SparkBase.MotorType.kBrushless
    )
    self.TurnSparkMax: rev.SparkBase = rev.SparkBase(
      TurnMotorChannel, rev.SparkBase.MotorType.kBrushless
    )

    """ Initialize Spark Max encoders"""
    # Get Encoder Objects from Spark Max
    self.DriveEncoder: rev.SparkRelativeEncoder = self.DriveSparkMax.getEncoder(
      # rev.SparkMaxRelativeEncoder.Type.kHallSensor
    )
    self.TurnEncoder: rev.SparkAbsoluteEncoder = self.TurnSparkMax.getAbsoluteEncoder(
      # rev.SparkMaxAbsoluteEncoder.Type.kDutyCycle
    )

    # Apply position and velocity conversion factors for the Drive encoder.
    # We want these in radians and radians per second to use with WPILibs swerve APIs
    # self.DriveEncoder.positionConversionFactor(
    #   constants.kDriveEncoderPositionFactor
    # )
    # self.DriveEncoder.setVelocityConversionFactor(
    #   constants.kDriveEncoderVelocityFactor
    # )

    # Apply position and velocity conversion factors for the Drive encoder.
    # We want these in radians and radians per second to use with WPILibs swerve APIs
    # self.TurnEncoder.PositionConversionFactor(
    #   constants.kTurnEncoderPositionFactor
    # )
    # self.TurnEncoder.setVelocityConversionFactor(
    #   constants.kTurnEncoderVelocityFactor
    # )

    # Invert the Turn encoder, since the output shaft rotates in the opposite
    # direction of the steering motor in the MAXSwerve Module.
    self.TurnEncoder.setInverted(constants.kTurnEncoderInverted)

    """ Initialize PID Controllers"""
    # create spark max pid controllers
    self.DriveClosedLoopController = self.DriveSparkMax.getClosedLoopController()

    self.TurnClosedLoopController = self.TurnSparkMax.getClosedLoopController()

    # Enable PID wrap around for the Turn motor. This will allow the PID
    # controller to go through 0 to get to the setpoint i.e. going from 350
    # degrees to 10 degrees will go through 0 rather than the other direction
    #  which is a longer route.
    # self.TurnClosedLoopController.__setattr__(
    #   rev._rev.ClosedLoopConfig.positionWrappingEnabled, True
    # )
    # self.TurnClosedLoopController.__setattr__(
    #   rev._rev.ClosedLoopConfig.positionWrappingInputRange(
    #     constants.kTurnEncoderPositionPIDMinInput,
    #     constants.kTurnEncoderPositionPIDMaxInput,
    #   )
    # )
    # self.TurnClosedLoopController.__setattr__(
    #   rev._rev.ClosedLoopConfig.positionWrappingMaxInput,
    #   constants.kTurnEncoderPositionPIDMaxInput,
    # )

    # # Set the PID Controller to use the duty cycle encoder on the swerve
    # # module instead of the built in NEO550 encoder.
    # self.TurnClosedLoopController.setFeedbackDevice(self.TurnEncoder)

    # # Set the PID gains for the Drive motor. Note these are example gains, and
    # # you may need to tune them for your own robot!
    # self.DriveClosedLoopController.setP(constants.kDriveP)
    # self.DriveClosedLoopController.setI(constants.kDriveI)
    # self.DriveClosedLoopController.setD(constants.kDriveD)
    # self.DriveClosedLoopController.setFF(constants.kDriveFF)
    # self.DriveClosedLoopController.setOutputRange(
    #   constants.kDriveMinOutput, constants.kDriveMaxOutput
    # )

    # # Set the PID gains for the Turn motor. Note these are example gains, and
    # # you may need to tune them for your own robot!
    # self.TurnClosedLoopController.setP(constants.kTurnP)
    # self.TurnClosedLoopController.setI(constants.kTurnI)
    # self.TurnClosedLoopController.setD(constants.kTurnD)
    # self.TurnClosedLoopController.setFF(constants.kTurnFF)
    # self.TurnClosedLoopController.setOutputRange(
    #   constants.kTurnMinOutput, constants.kTurnMaxOutput
    # )

    # """ Spark Max Mode Parameters"""
    # self.DriveSparkMax.setIdleMode(constants.kDriveMotorIdleMode)
    # self.TurnSparkMax.setIdleMode(constants.kTurnMotorIdleMode)
    # self.DriveSparkMax.setSmartCurrentLimit(constants.kDriveMotorCurrentLimit)
    # self.TurnSparkMax.setSmartCurrentLimit(constants.kDriveMotorCurrentLimit)

    # # Save the SPARK MAX configurations. If a SPARK MAX browns out during
    # # operation, it will maintain the above configurations
    # self.DriveSparkMax.burnFlash()
    # self.TurnSparkMax.burnFlash()

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
    optimizedDesiredState = wpimath.kinematics.SwerveModuleState.optimize(
      correctedDesiredState, TurnEncoderPosition
    )

    # Command Drive and Turn SPARK MAX toward their respective setpoints
    self.DriveClosedLoopController.setReference(
      optimizedDesiredState.speed, rev.SparkBase.ControlType.kVelocity
    )
    self.TurnClosedLoopController.setReference(
      optimizedDesiredState.angle.radians(), rev.CANSparkMax.ControlType.kPosition
    )

    self.desiredState = desiredState

  def resetEncoders(self) -> None:
    self.DriveEncoder.setPosition(0)
