from commands2 import Subsystem
from rev import (
  SparkBase,
  SparkMax,
)

from config import Config
from constants import PickupSubsystemConstants


class PickupSubsystem(Subsystem):
  def __init__(self):
    super().__init__()

    self.upperPickupMotor = SparkMax(
      PickupSubsystemConstants.kUpperPickupMotorId, SparkMax.MotorType.kBrushless
    )
    self.lowerPickupMotor = SparkMax(
      PickupSubsystemConstants.kLowerPickupMotorId, SparkMax.MotorType.kBrushless
    )

    ### Encoders ###
    self.upperPickupMotor.getEncoder()
    self.lowerPickupMotor.getEncoder()

    ### Apply Configs ###
    self.upperPickupMotor.configure(
      Config.PickupSubsystem.upperMotorConfig,
      SparkBase.ResetMode.kResetSafeParameters,
      SparkBase.PersistMode.kPersistParameters,
    )
    self.lowerPickupMotor.configure(
      Config.PickupSubsystem.lowerMotorConfig,
      SparkBase.ResetMode.kResetSafeParameters,
      SparkBase.PersistMode.kPersistParameters,
    )

  def manualDrive(self, speed: float):
    """
    Drives the intake to pull or push based on user input.

    ::param speed: User input speed. (-1 - 1)
    """
    deliveredSpeed = speed * PickupSubsystemConstants.kManualPickupSpeed

    self.upperPickupMotor.set(deliveredSpeed)
    self.lowerPickupMotor.set(deliveredSpeed)

  def stop(self):
    self.upperPickupMotor.set(0)
    self.lowerPickupMotor.set(0)
