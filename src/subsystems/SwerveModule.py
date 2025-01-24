import math

import wpilib
import wpimath.controller
import wpimath.geometry
import wpimath.kinematics
import wpimath.trajectory

from constants import SwerveModuleConstants


class SwerveModule:
  def __init__(
    self,
    driveMotorId: int,
    turnMotorId: int,
    driveEncoderAId: int,
    driveEncoderBId: int,
    turnEncoderAId: int,
    turnEncoderBId: int,
  ):
    """Constructs a SwerveModule with a drive motor, turning motor, drive encoder and turning encoder.

    :param driveMotorId:      PWM output for the drive motor.
    :param turnMotorId:    PWM output for the turning motor.
    :param driveEncoderAId:   DIO input for the drive encoder A
    :param driveEncoderBId:   DIO input for the drive encoder B
    :param turnEncoderAId: DIO input for the turning encoder A
    :param turnEncoderBId: DIO input for the turning encoder B
    """
    self.driveMotor = wpilib.PWMTalonFX(driveMotorId)
    self.turnMotor = wpilib.PWMSparkMax(turnMotorId)

    self.driveEncoder = wpilib.Encoder(driveEncoderAId, driveEncoderBId)

    self.turningEncoder = wpilib.Encoder(turnEncoderAId, turnEncoderBId)

    # TODO: ALL PID CONTROLLERS MUST BE CALIBRATED
    self.drivePIDController = wpimath.controller.PIDController(1, 0, 0)

    # TODO: ALL PID CONTROLLERS MUST BE CALIBRATED
    self.turningPIDController = wpimath.controller.ProfiledPIDController(
      1,
      0,
      0,
      wpimath.trajectory.TrapezoidProfile.Constraints(
        SwerveModuleConstants.kModuleMaxAngularVelocity,
        SwerveModuleConstants.kModuleMaxAngularAcceleration,
      ),
    )

    # TODO: ALL PID CONTROLLERS MUST BE CALIBRATED
    self.driveFeedforward = wpimath.controller.SimpleMotorFeedforwardMeters(1, 3)
    self.turnFeedforward = wpimath.controller.SimpleMotorFeedforwardMeters(1, 0.5)

    # Set the distance per pulse for the drive encoder. We can simply use the distance traveled for one rotation of the wheel divided by the encoder resolution.
    self.driveEncoder.setDistancePerPulse(
      (math.tau * SwerveModuleConstants.kWheelRadius)
      / SwerveModuleConstants.kEncoderResolution
    )

    # Set the distance (in this case, angle) in radians per pulse for the turning encoder. This is the the angle through an entire rotation (2 * pi) divided by the encoder resolution.
    self.turningEncoder.setDistancePerPulse(
      math.tau / SwerveModuleConstants.kEncoderResolution
    )

    # Limit the PID Controller's input range between -pi and pi and set the input to be continuous.
    self.turningPIDController.enableContinuousInput(-math.pi, math.pi)

  def getState(self) -> wpimath.kinematics.SwerveModuleState:
    """Returns the current state of the module.

    :returns: The current state of the module.
    """
    return wpimath.kinematics.SwerveModuleState(
      self.driveEncoder.getRate(),
      wpimath.geometry.Rotation2d(self.turningEncoder.getDistance()),
    )

  def getPosition(self) -> wpimath.kinematics.SwerveModulePosition:
    """Returns the current position of the module.

    :returns: The current position of the module.
    """
    return wpimath.kinematics.SwerveModulePosition(
      self.driveEncoder.getDistance(),
      wpimath.geometry.Rotation2d(self.turningEncoder.getDistance()),
    )

  def setDesiredState(self, desiredState: wpimath.kinematics.SwerveModuleState) -> None:
    """Sets the desired state for the module.

    :param desiredState: Desired state with speed and angle.
    """

    encoderRotation = wpimath.geometry.Rotation2d(self.turningEncoder.getDistance())

    # Optimize the reference state to avoid spinning further than 90 degrees
    desiredState.optimize(encoderRotation)

    # Scale speed by cosine of angle error. This scales down movement perpendicular to the desired direction of travel that can occur when modules change directions. This results in smoother driving.
    desiredState.cosineScale(encoderRotation)

    # Calculate the drive output from the drive PID controller.
    driveOutput = self.drivePIDController.calculate(
      self.driveEncoder.getRate(), desiredState.speed
    )

    driveFeedforward = self.driveFeedforward.calculate(desiredState.speed)

    # Calculate the turning motor output from the turning PID controller.
    turnOutput = self.turningPIDController.calculate(
      self.turningEncoder.getDistance(), desiredState.angle.radians()
    )

    turnFeedforward = self.turnFeedforward.calculate(
      self.turningPIDController.getSetpoint().velocity
    )

    self.driveMotor.setVoltage(driveOutput + driveFeedforward)
    self.turnMotor.setVoltage(turnOutput + turnFeedforward)
