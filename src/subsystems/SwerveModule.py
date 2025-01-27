from phoenix6 import configs, controls, hardware
from rev import SparkBase, SparkLowLevel, SparkMax
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.units import radiansToDegrees

from config import Config
from constants import SwerveModuleConstants


class SwerveModule:
  def __init__(
    self,
    turnMotorId: int,
    driveMotorId: int,
    chassisAngularOffset: int = 0,
    invertTurnEncoder: bool = False,
  ):
    """Constructs a SwerveModule with a drive motor, turning motor, drive encoder and turning encoder.

    :param driveMotorId:      PWM output for the drive motor.
    :param turnMotorId:    PWM output for the turning motor.
    :param invertTurnEncoder:   Inverts the turning encoder.
    :param chassisAngularOffset: The angle of the module relative to the chassis (radians).
    """
    self.chassisAngularOffset = chassisAngularOffset
    self.desiredState = SwerveModuleState(0.0, Rotation2d())

    ### Motors and Configuration ###
    self.driveMotor = hardware.TalonFX(driveMotorId)
    self.turnMotor = SparkMax(
      turnMotorId,
      SparkMax.MotorType.kBrushless,
    )

    # Turning encoder should be inverted if the output shaft rotates in the opposite direction of the steering motor.
    Config.MAXSwerveModule.turnConfig.absoluteEncoder.inverted(invertTurnEncoder)
    self.turnMotor.configure(
      Config.MAXSwerveModule.turnConfig,
      SparkBase.ResetMode.kResetSafeParameters,
      SparkBase.PersistMode.kPersistParameters,
    )

    # Any unmodified configs in a configuration object are *automatically* factory-defaulted. If you want to explicitly factory reset the config, use: self.driveMotor.configurator.apply(configs.TalonFXConfiguration())
    self.driveMotor.configurator.apply(Config.MAXSwerveModule.driveMotorConfig)

    ### Encoders ### (Talon FX encoder is built in, no need to store it)
    self.turnEncoder = self.turnMotor.getAbsoluteEncoder()

    ### Closed Loop Controllers ### (Drive Motor can only get the CLC output)
    self.turnClosedLoopController = self.turnMotor.getClosedLoopController()

    self.desiredState.angle = Rotation2d(self.turnEncoder.getPosition())
    self.driveMotor.set_position(0)

  def getState(self) -> SwerveModuleState:
    """Returns the current state of the module.

    :returns: The current state of the module.
    """
    # TODO: self.driveMotor.get_velocity() needs to be converted to m/s. See: https://github.com/REVrobotics/MAXSwerve-Java-Template/blob/main/src/main/java/frc/robot/Configs.java
    return SwerveModuleState(
      self.driveMotor.get_velocity(),
      Rotation2d(self.turnEncoder.getPosition() - self.chassisAngularOffset),
    )

  def getPosition(self) -> SwerveModulePosition:
    """Returns the current position of the module.

    :returns: The current position of the module.
    """
    # TODO: self.driveMotor.get_position() needs to be converted to meters. See: https://github.com/REVrobotics/MAXSwerve-Java-Template/blob/main/src/main/java/frc/robot/Configs.java
    return SwerveModulePosition(
      self.driveMotor.get_position(),
      Rotation2d(self.turnEncoder.getPosition() - self.chassisAngularOffset),
    )

  def setDesiredState(self, desiredState: SwerveModuleState) -> None:
    """Sets the desired state for the module.

    :param desiredState: Desired state with speed and angle.
    """
    correctedDesiredState = SwerveModuleState()
    correctedDesiredState.speed = desiredState.speed
    correctedDesiredState.angle = desiredState.angle.__add__(
      Rotation2d.fromDegrees(radiansToDegrees(self.chassisAngularOffset))
    )

    # Optimize the reference state to avoid spinning further than 90 degrees.
    correctedDesiredState.optimize(Rotation2d(self.turnEncoder.getPosition()))

    # Command driving and turning motors towards their respective setpoints.
    # TODO: Need to convert correctedDesiredState from m/s to native units.
    # wheelCircumference = 0.1  # Example value, replace with your actual wheel circumference in meters
    # rotationsPerMeter = 1 / wheelCircumference
    # speedRotationsPerSecond = correctedDesiredState.speed * rotationsPerMeter
    self.driveMotor.set_control(controls.VelocityDutyCycle(correctedDesiredState.speed))
    self.turnClosedLoopController.setReference(
      correctedDesiredState.angle.radians(), SparkLowLevel.ControlType.kPosition
    )

    self.desiredState = desiredState

  def resetDriveEncoder(self) -> None:
    """Resets the encoders on the module."""
    self.driveMotor.set_position(0)
