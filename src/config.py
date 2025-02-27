import math

from rev import ClosedLoopConfig, SparkBaseConfig

from constants import SwerveModuleConstants


class Config:
  class MAXSwerveModule:
    ### Drive Motor Configurations ###
    kTurningFactor = 2 * math

    turnConfig = SparkBaseConfig()
    turnConfig.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(20)

    turnConfig.absoluteEncoder.inverted(True).positionConversionFactor(
      kTurningFactor
    ).velocityConversionFactor(kTurningFactor / 60.0)  # Radians per Second

    # TODO: Calibrate PID Controller
    turnConfig.closedLoop.setFeedbackSensor(
      ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder
    ).pid(1, 0, 0).outputRange(-1, 1).positionWrappingEnabled(
      True
    ).positionWrappingInputRange(0, kTurningFactor)

    ### Trun Motor Config ###
    drivingFactor = (
      SwerveModuleConstants.kWheelDiameter / SwerveModuleConstants.kDriveMotorReduction
    )
    drivingVelocityFeedForward = 0
    driveConfig = SparkBaseConfig()

    driveConfig.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(
      50
    ).inverted(True)

    driveConfig.encoder.positionConversionFactor(
      drivingFactor
    ).velocityConversionFactor(drivingFactor / 60)

    driveConfig.closedLoop.setFeedbackSensor(
      ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder
    ).pid(0.04, 0, 0).velocityFF(drivingVelocityFeedForward).outputRange(-1, 1)
