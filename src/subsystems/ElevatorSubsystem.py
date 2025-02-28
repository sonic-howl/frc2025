from commands2 import Subsystem
from rev import (
  SparkBase,
  SparkClosedLoopController,
  SparkMax,
)
from wpimath.controller import ElevatorFeedforward

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
    self.elevatorEncoder = self.elevatorMotor.getEncoder()

    ### Closed Loop Controllers ###
    self.elevatorClosedLoopController = self.elevatorMotor.getClosedLoopController()

    ### Elevator Feed Forward ###
    # https://docs.wpilib.org/en/stable/docs/software/advanced-controls/introduction/tuning-elevator.html
    self.feedForward = ElevatorFeedforward(0, 0, 0, 0)

  def manualDrive(self, speed: int):
    """
    Raises or Lowers the elevator at the speed determined by manua user input.

    ::param speed: User input speed from controller. (-1 to 1)"""
    deliveredSpeed = speed * ElevatorSubsystemConstants.kManualElevatorSpeed

    self.elevatorMotor.set(deliveredSpeed)

  def goToPosition(self, position: float):
    """
    Raises or Lowers the elevator to the provided posistion.

    ::param position: Desired Position"""
    self.elevatorClosedLoopController.setReference(
      position,
      SparkMax.ControlType.kMAXMotionPositionControl,
      arbFeedforward=self.feedForward,
      arbFFUnits=SparkClosedLoopController.ArbFFUnits.kVoltage,
    )

  def stop(self):
    self.elevatorMotor.set(0)
