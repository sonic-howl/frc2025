from rev import (
  SparkBase,
  SparkLowLevel,
  SparkMax,
)
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.units import radiansToDegrees

from config import Config


class SwerveModule:
  def __init__(
    self,
    driveMotorId: int,
    turnMotorId: int,
    chassisAngularOffset: float = 0,
  ):
    """Constructs a SwerveModule with a drive motor, turning motor, drive encoder and turning encoder.

    :param driveMotorId
    :param turnMotorId
    :param chassisAngularOffset: The angle of the module relative to the chassis (radians).
    :param invertTurnEncoder:   Inverts the turning encoder.
    """
    self.chassisAngularOffset = chassisAngularOffset
    self.desiredState = SwerveModuleState(0.0, Rotation2d())

    ### Motors and Configuration ###
    self.driveMotor = SparkMax(driveMotorId, SparkMax.MotorType.kBrushless)
    self.turnMotor = SparkMax(turnMotorId, SparkMax.MotorType.kBrushless)

    # Any unmodified configs in a configuration object are *automatically* factory-defaulted. If you want to explicitly factory reset the config, use: self.driveMotor.configurator.apply(configs.TalonFXConfiguration())
    # self.driveMotor.configurator.apply(Config.TalonSwerveModule.driveConfig)
    ### Encoders ###
    self.driveEncorder = self.driveMotor.getEncoder()
    self.turnEncoder = self.turnMotor.getAbsoluteEncoder()

    ### Closed Loop Controllers ### (Drive Motor can only get the CLC output, not the CLC object)
    self.driveClosedLoopController = self.driveMotor.getClosedLoopController()
    self.turnClosedLoopController = self.turnMotor.getClosedLoopController()

    ### Apply Motor Controller Configs ###
    self.driveMotor.configure(
      Config.MAXSwerveModule.driveConfig,
      SparkBase.ResetMode.kResetSafeParameters,
      SparkBase.PersistMode.kPersistParameters,
    )

    self.turnMotor.configure(
      Config.MAXSwerveModule.turnConfig,
      SparkBase.ResetMode.kResetSafeParameters,
      SparkBase.PersistMode.kPersistParameters,
    )

    self.desiredState.angle = Rotation2d(self.turnEncoder.getPosition())
    self.resetDriveEncoder()

  def getState(self) -> SwerveModuleState:
    """Returns the current state of the module."""

    return SwerveModuleState(
      self.driveEncorder.getVelocity(),
      Rotation2d(self.turnEncoder.getPosition() - self.chassisAngularOffset),
    )

  def getPosition(self) -> SwerveModulePosition:
    """Returns the current position of the module."""

    return SwerveModulePosition(
      self.driveEncorder.getPosition(),
      Rotation2d(self.turnEncoder.getPosition() - self.chassisAngularOffset),
    )

  def setDesiredState(self, desiredState: SwerveModuleState) -> None:
    """Sets the desired state for the module.

    :param desiredState: Desired state with speed and angle.
    """
    correctDesiredState = SwerveModuleState()
    correctDesiredState.speed = desiredState.speed
    correctDesiredState.angle = desiredState.angle.__add__(Rotation2d.fromDegrees(radiansToDegrees(self.chassisAngularOffset)))

    # Optimize the reference state to avoid spinning further than 90 degrees.
    correctDesiredState.optimize(Rotation2d(self.turnEncoder.getPosition()))

    # Command driving and turning motors towards their respective setpoints.
    self.driveClosedLoopController.setReference(correctDesiredState.speed, SparkLowLevel.ControlType.kVelocity)
    self.turnClosedLoopController.setReference(correctDesiredState.angle.radians(), SparkLowLevel.ControlType.kPosition)

    self.desiredState = desiredState

  def resetDriveEncoder(self) -> None:
    self.driveEncorder.setPosition(0)
