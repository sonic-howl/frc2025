import rev
from commands2 import Subsystem

from constants import ElevatorSubsystemConstants, PickupSubsystemConstants


class ElevatorSubsystem(Subsystem):
  def __init__(self):
    super().__init__()

    self.speed = ElevatorSubsystemConstants.kElevatorSpeed

    self.leftElevatorMotor = rev.SparkMax(ElevatorSubsystemConstants.kLeftElevatorMotorId, rev.SparkMax.MotorType.kBrushless)
    self.rightElevatorMotor = rev.SparkMax(
      ElevatorSubsystemConstants.kRightElevatorMotorId,
      rev.SparkMax.MotorType.kBrushless,
    )

  def drive(self, inverted: bool = False):
    """
    Raises or Lowers the elevator assembly at a constant speed

    ::param inverted: Wether to raise or lower the assembly. Lowers
    """

    # TODO: Make controller rumble when the limit switch is pressed.
    if inverted:
      self.leftElevatorMotor.set(self.speed)
      self.rightElevatorMotor.set(self.speed)
    else:
      self.leftElevatorMotor.set(-self.speed)
      self.rightElevatorMotor.set(-self.speed)

  def release(self):
    pass

  def stop(self):
    self.leftElevatorMotor.set(0)
    self.rightElevatorMotor.set(0)


class PickupSubsystem(Subsystem):
  def __init__(self):
    super().__init__()

    self.speed = PickupSubsystemConstants.kPickupSpeed

    self.upperPickupMotor = rev.SparkMax(PickupSubsystemConstants.kUpperPickupMotorId, rev.SparkMax.MotorType.kBrushless)
    self.lowerPickupMotor = rev.SparkMax(PickupSubsystemConstants.kLowerPickupMotorId, rev.SparkMax.MotorType.kBrushless)

  def drive(self, inverted: bool = False):
    """
    Pulls or Pushes the intake at a constant speed

    :param inverted: Wether to pull or push. Pushes by default.
    """

    # TODO: Make controller rumble when the limit switch is pressed.
    if inverted:
      self.upperPickupMotor.set(-self.speed)
      self.lowerPickupMotor.set(self.speed)
    else:
      self.upperPickupMotor.set(self.speed)
      self.lowerPickupMotor.set(-self.speed)

  def stop(self):
    self.upperPickupMotor.set(0)
    self.lowerPickupMotor.set(0)
