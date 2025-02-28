import math

from rev import ClosedLoopConfig, SparkBaseConfig

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
    leftMotorVelocityFeedForward = 0

    leftMotorConfig = SparkBaseConfig()

    leftMotorConfig.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(50).inverted(
      True
    )

    # leftMotorConfig.encoder.positionConversionFactor(
    #   driveFactor
    # ).velocityConversionFactor(driveFactor / 60)

    leftMotorConfig.closedLoop.setFeedbackSensor(
      ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder
    ).pid(
      ElevatorSubsystemConstants.kP, ElevatorSubsystemConstants.kI, ElevatorSubsystemConstants.kD
    ).velocityFF(leftMotorVelocityFeedForward).outputRange(-1, 1)

    ### Right Motor Config ###
    rightMotorVelocityFeedForward = 0

    rightMotorConfig = SparkBaseConfig()

    rightMotorConfig.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(50).inverted(
      True
    )

    # rightMotorConfig.encoder.positionConversionFactor(
    #   driveFactor
    # ).velocityConversionFactor(driveFactor / 60)

    rightMotorConfig.closedLoop.setFeedbackSensor(
      ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder
    ).pid(
      ElevatorSubsystemConstants.kP, ElevatorSubsystemConstants.kI, ElevatorSubsystemConstants.kD
    ).velocityFF(rightMotorConfig).outputRange(-1, 1)

  class PickupSubsystem:
    ### Lower Motor Config ###
    lowerMotorConfig = SparkBaseConfig()

    ### Upper Motor Config ###
    upperMotorConfig = SparkBaseConfig()
