import math

from pathplannerlib.config import PIDConstants
from rev import ClosedLoopConfig, SparkBaseConfig, SparkMaxConfig

from constants import ElevatorSubsystemConstants, SwerveModuleConstants


class Config:
  class MAXSwerveModule:
    ### Drive Motor Configurations ###
    drivingFactor = (
      SwerveModuleConstants.kWheelDiameter / SwerveModuleConstants.kDriveMotorReduction
    )
    drivingVelocityFeedForward = 0

    driveConfig = SparkBaseConfig()
    driveConfig.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(50).inverted(False)

    driveConfig.encoder.positionConversionFactor(drivingFactor).velocityConversionFactor(
      drivingFactor / 60
    )

    driveConfig.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder).pid(
      0.1, 0, 0
    ).velocityFF(drivingVelocityFeedForward).outputRange(-1, 1)

    ### Trun Motor Config ###
    kTurningFactor = 2 * math.pi

    turnConfig = SparkBaseConfig()
    turnConfig.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(20)

    turnConfig.absoluteEncoder.inverted(True).positionConversionFactor(
      kTurningFactor
    ).velocityConversionFactor(kTurningFactor / 60.0)  # Radians per Second

    # TODO: Calibrate PID Controller
    turnConfig.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder).pid(
      1, 0, 0
    ).outputRange(-1, 1).positionWrappingEnabled(True).positionWrappingInputRange(0, kTurningFactor)

  class ElevatorSubsystem:
    # driveFactor = (
    #   ElevatorSubsystemConstants.kWheelDiameter / ElevatorSubsystemConstants.kDriveMotorReduction
    # )

    ### Left Motor Config ##
    MotorVelocityFeedForward = 0

    leftMotorConfig = SparkMaxConfig()

    leftMotorConfig.setIdleMode(SparkMaxConfig.IdleMode.kBrake).smartCurrentLimit(50).inverted(True)

    # leftMotorConfig.softLimit.forwardSoftLimit(
    #   ElevatorSubsystemConstants.kMotorForwardSoftLimit
    # ).reverseSoftLimit(ElevatorSubsystemConstants.kMotorReverseSoftLimit).forwardSoftLimitEnabled(
    #   True
    # ).reverseSoftLimitEnabled(True)

    leftMotorConfig.closedLoop.setFeedbackSensor(
      ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder
    ).pid(
      ElevatorSubsystemConstants.kP, ElevatorSubsystemConstants.kI, ElevatorSubsystemConstants.kD
    ).velocityFF(ElevatorSubsystemConstants.kMotorVelocityFeedForward).outputRange(-1, 1)
    leftMotorConfig.closedLoop.maxMotion.maxVelocity(
      ElevatorSubsystemConstants.kMotorMaxVelocity
    ).maxAcceleration(ElevatorSubsystemConstants.kMotorAcceleration)

    ### Right Motor Config ###

    rightMotorConfig = SparkMaxConfig()

    rightMotorConfig.setIdleMode(SparkMaxConfig.IdleMode.kBrake).follow(
      ElevatorSubsystemConstants.kLeftElevatorMotorId, True
    )

  class PickupSubsystem:
    ### Lower Motor Config ###
    lowerMotorConfig = SparkBaseConfig()

    ### Upper Motor Config ###
    upperMotorConfig = SparkBaseConfig().inverted(True)

  class DriveSubsystem:
    translationPPHolonominicDrivePID = PIDConstants(5.0, 0.0, 0.0)
    rotationPPHolonominicDrivePID = PIDConstants(5.0, 0.0, 0.0)
