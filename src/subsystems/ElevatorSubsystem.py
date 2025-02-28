from commands2 import Subsystem
from rev import SparkBase, SparkMax

from config import Config
from constants import ElevatorSubsystemConstants


class ElevatorSubsystem(Subsystem):
  def __init__(self):
    super().__init__()

    leftElevatorMotor = SparkMax(
      ElevatorSubsystemConstants.kLeftElevatorMotorId, SparkMax.MotorType.kBrushless
    )
    rightElevatorMotor = SparkMax(
      ElevatorSubsystemConstants.kRightElevatorMotorId,
      SparkMax.MotorType.kBrushless,
    )

    ### Apply Configs ###
    leftElevatorMotor.configure(
      Config.ElevatorSubsystem.leftMotorConfig,
      SparkBase.ResetMode.kResetSafeParameters,
      SparkBase.PersistMode.kPersistParameters,
    )
    rightElevatorMotor.configure(
      Config.ElevatorSubsystem.rightMotorConfig,
      SparkBase.ResetMode.kResetSafeParameters,
      SparkBase.PersistMode.kPersistParameters,
    )

    self.elevatorMotor = leftElevatorMotor

    ### Encoders ###
    self.elevatorEncoder = leftElevatorMotor.getEncoder()

    ### Closed Loop Controllers ###
    self.elevatorClosedLoopController = leftElevatorMotor.getClosedLoopController()

  def manualDrive(self, speed: int):
    """
    Raises or Lowers the elevator at the speed determined by manua user input.

    ::param speed: User input speed from controller. (-1 to 1)"""
    deliveredSpeed = speed * ElevatorSubsystemConstants.kManualElevatorSpeed

    self.elevatorMotor.set(deliveredSpeed)

  def stop(self):
    self.elevatorMotor.set(0)
