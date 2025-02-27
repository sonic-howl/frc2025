import math

from rev import AbsoluteEncoderConfig, ClosedLoopConfig, EncoderConfig, SparkBaseConfig

from constants import SwerveModuleConstants


class Config:
  class MAXSwerveModule:
    kTurningFactor = 2 * math.pi

    turnConfig = SparkBaseConfig()
    turnConfig.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(20)

    turnEncoderConfig = AbsoluteEncoderConfig()
    turnEncoderConfig.inverted(True).positionConversionFactor(kTurningFactor).velocityConversionFactor(kTurningFactor / 60.0)  # Radians per Second
    turnConfig.apply(turnEncoderConfig)

    # TODO: Calibrate PID Controller
    turnClosedLoopConfig = ClosedLoopConfig()
    turnClosedLoopConfig.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder).pid(1, 0, 0).outputRange(-1, 1).positionWrappingEnabled(True).positionWrappingInputRange(0, kTurningFactor)
    turnConfig.apply(turnClosedLoopConfig)

    driveConfig = SparkBaseConfig()
    drivingFactor = SwerveModuleConstants.kWheelDiameter / SwerveModuleConstants.kDriveMotorReduction

    drivingVelocityFeedForward = 0

    driveConfig.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(50)

    driveEncoderConfig = EncoderConfig()
    driveEncoderConfig.positionConversionFactor(drivingFactor)
    driveEncoderConfig.velocityConversionFactor(drivingFactor / 60)
    driveConfig.apply(driveEncoderConfig)

    driveClosedLoopConfig = ClosedLoopConfig()
    driveClosedLoopConfig.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder).pid(0.04, 0, 0).velocityFF(drivingVelocityFeedForward).outputRange(-1, 1)
    driveConfig.apply(driveClosedLoopConfig)
