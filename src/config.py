import math

from phoenix6 import configs
from phoenix6.signals import FeedbackSensorSourceValue
from phoenix6.signals.spn_enums import NeutralModeValue
from rev import ClosedLoopConfig, SparkBaseConfig, SparkMaxConfig


class Config:
  class MAXSwerveModule:
    turnConfig = SparkMaxConfig()

    kTurningFactor = 2 * math.pi

    turnConfig.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(20)

    turnConfig.absoluteEncoder.inverted(True).positionConversionFactor(
      kTurningFactor
    ).velocityConversionFactor(kTurningFactor / 60.0)  # Radians per Second

    # TODO: Calibrate PID Controller
    turnConfig.closedLoop.setFeedbackSensor(
      ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder
    ).pid(0, 0, 0).outputRange(-1, 1).positionWrappingEnabled(
      True
    ).positionWrappingInputRange(0, kTurningFactor)

  class TalonSwerveModule:
    driveConfig = configs.TalonFXConfiguration()

    driveConfig.feedback.feedback_sensor_source = FeedbackSensorSourceValue.ROTOR_SENSOR

    # Might be needed to convert sensor values to useful units
    # driveConfig.feedback.sensor_to_mechanism_ratio

    driveConfig.motor_output.neutral_mode = NeutralModeValue.BRAKE
    # driveConfig.voltage.peak_forward_voltage = 16
    # driveConfig.voltage.peak_reverse_voltage = -16
    driveConfig.current_limits.stator_current_limit = 120  # AMPS
    driveConfig.current_limits.stator_current_limit_enable = True
    driveConfig.current_limits.supply_current_limit = 70  # AMPS
    driveConfig.current_limits.supply_current_limit_enable = True

    # Closed Loop Control
    driveConfig.slot0.k_p = 0.1
    driveConfig.slot0.k_d = 0
    driveConfig.slot0.k_i = 0
    # driveConfig.slot0.k_v = 0 #TODO: Needs Calibration
