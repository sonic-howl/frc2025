import math

from phoenix6 import configs
from phoenix6.signals.spn_enums import NeutralModeValue
from rev import ClosedLoopConfig, SparkBaseConfig, SparkMaxConfig


class Config:
  class MAXSwerveModule:
    ### Turning Motor and Encoder Config ###
    turnConfig = SparkMaxConfig()
    kTurningFactor = 2 * math.pi

    turnConfig.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(20)

    turnConfig.absoluteEncoder.positionConversionFactor(
      kTurningFactor
    ).velocityConversionFactor(kTurningFactor / 60.0)  # Radians per second

    # Remember to calibrate the PID values.
    # Enable PID wrap around for the turning motor. This will allow the PID controller to go through 0 to get to the setpoint i.e. going from 350 degrees to 10 degrees will go through 0 rather than the other direction which is a longer route.
    turnConfig.closedLoop.setFeedbackSensor(
      ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder
    ).pid(1, 0, 0).outputRange(-1, 1).positionWrappingEnabled(
      True
    ).positionWrappingInputRange(0, kTurningFactor)

    ### Drive Motor and Encoder Config ###
    driveMotorConfig = configs.TalonFXConfiguration()

    # kDrivingVelocityFeedForward = None

    driveMotorConfig.feedback.sensor_to_mechanism_ratio

    driveMotorConfig.motor_output.neutral_mode = NeutralModeValue.BRAKE
    # driveMotorConfig.voltage.peak_forward_voltage = 16
    # driveMotorConfig.voltage.peak_reverse_voltage = -16
    driveMotorConfig.current_limits.stator_current_limit = 120
    driveMotorConfig.current_limits.stator_current_limit_enable = True
    driveMotorConfig.current_limits.supply_current_limit = 70
    driveMotorConfig.current_limits.supply_current_limit_enable = True

    # Closed Loop Control
    driveMotorConfig.slot0.k_p = 0
    driveMotorConfig.slot0.k_d = 0
    driveMotorConfig.slot0.k_i = 0
    driveMotorConfig.closed_loop_general.continuous_wrap
    # driveMotorConfig.slot0.k_v = kDrivingVelocityFeedForward
