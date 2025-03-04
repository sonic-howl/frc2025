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

  def pull(self):
    """
    Drives the intake at a constant speed, in order to pull the game piece into the bot.
    """
    self.upperPickupMotor.set(PickupSubsystemConstants.kPickupSpeed)
    self.lowerPickupMotor.set(PickupSubsystemConstants.kPickupSpeed)

  def push(self):
    """
    Drives the intake at a constant speed, in order to pushes the game piece into the bot.
    """
    self.upperPickupMotor.set(-PickupSubsystemConstants.kPickupSpeed)
    self.lowerPickupMotor.set(-PickupSubsystemConstants.kPickupSpeed)

  def stop(self):
    self.upperPickupMotor.set(0)
    self.lowerPickupMotor.set(0)

  def release(self):
    pass
