from commands2 import Subsystem
from rev import (
  SparkBase,
  SparkMax,
)

from config import Config
from constants import ElevatorSubsystemConstants


class ElevatorSubsystem(Subsystem):
  def __init__(self):
    super().__init__()

    self.leftElevatorMotor = SparkMax(ElevatorSubsystemConstants.kLeftElevatorMotorId, SparkMax.MotorType.kBrushless)
    self.rightElevatorMotor = SparkMax(
      ElevatorSubsystemConstants.kRightElevatorMotorId,
      SparkMax.MotorType.kBrushless,
    )

    ### Encoders ###
    self.leftElevatorEncoder = self.leftElevatorMotor.getEncoder()
    self.rightElevatorEncoder = self.rightElevatorMotor.getEncoder()

    ### Closed Loop Controllers ###
    self.leftElevatorClosedLoopController = self.leftElevatorMotor.getClosedLoopController()
    self.rightElevatorClosedLoopController = self.rightElevatorMotor.getClosedLoopController()

    ### Apply Configs ###
    self.leftElevatorMotor.configure(
      Config.ElevatorSubsystem.leftMotorConfig,
      SparkBase.ResetMode.kResetSafeParameters,
      SparkBase.PersistMode.kPersistParameters,
    )
    self.rightElevatorMotor.configure(
      Config.ElevatorSubsystem.rightMotorConfig,
      SparkBase.ResetMode.kResetSafeParameters,
      SparkBase.PersistMode.kPersistParameters,
    )

  def manualDrive(self, speed: int):
    """
    Raises or Lowers the elevator at the speed determined by manua user input.

    ::param speed: User input speed from controller. (-1 to 1)"""
    deliveredSpeed = speed * ElevatorSubsystemConstants.kManualElevatorSpeed

    self.leftElevatorMotor.set(deliveredSpeed)
    self.rightElevatorMotor.set(deliveredSpeed)

  def stop(self):
    self.leftElevatorMotor.set(0)
    self.rightElevatorMotor.set(0)
