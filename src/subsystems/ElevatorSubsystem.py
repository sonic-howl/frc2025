from commands2 import Subsystem
from rev import (
  SparkBase,
  SparkClosedLoopController,
  SparkMax,
)
from wpilib import DigitalInput, SmartDashboard
from wpimath.controller import ElevatorFeedforward

from config import Config
from constants import ElevatorSubsystemConstants


class ElevatorSubsystem(Subsystem):
  upperElevatorSwitchTriggerCount = 0
  upperElevatorSwitchIncrementFlag = False

  def __init__(self):
    super().__init__()

    self.upperElevatorSwitch = DigitalInput(ElevatorSubsystemConstants.kUpperSwitchChannel)
    self.lowerElevatorSwitch = DigitalInput(ElevatorSubsystemConstants.kLowerSwitchChannel)

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

  def periodic(self):
    currentElevatorMotorSpeed = self.elevatorMotor.get()
    currentUpperElevatorSwitchStatus = self.upperElevatorSwitch.get()

    if currentUpperElevatorSwitchStatus and not ElevatorSubsystem.upperElevatorSwitchIncrementFlag:
      if currentElevatorMotorSpeed > 0:
        ElevatorSubsystem.upperElevatorSwitchTriggerCount += 1
        ElevatorSubsystem.upperElevatorSwitchIncrementFlag = True
      elif currentElevatorMotorSpeed < 0:
        ElevatorSubsystem.upperElevatorSwitchTriggerCount -= 1
        ElevatorSubsystem.upperElevatorSwitchIncrementFlag = True

      if ElevatorSubsystem.upperElevatorSwitchTriggerCount >= 2:
        currentCommand = self.getCurrentCommand()
        if currentCommand is not None:
          currentCommand.cancel()
        self.stop()
    elif (
      not currentUpperElevatorSwitchStatus and ElevatorSubsystem.upperElevatorSwitchIncrementFlag
    ):
      ElevatorSubsystem.upperElevatorSwitchIncrementFlag = False

    if self.lowerElevatorSwitch.get():
      currentCommand = self.getCurrentCommand()
      if currentCommand is not None:
        currentCommand.cancel()
      self.stop()
      self.zeroPosition()
      # ElevatorSubsystem.upperElevatorSwitchTriggerCount = 0

    SmartDashboard.putNumber(
      "Upper Elevator Switch Trigger Count", ElevatorSubsystem.upperElevatorSwitchTriggerCount
    )

  def zeroPosition(self):
    self.elevatorEncoder.setPosition(0)

  def manualDrive(self, speed: float):
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
      arbFeedforward=self.feedForward.calculate(self.elevatorEncoder.getVelocity()),
      arbFFUnits=SparkClosedLoopController.ArbFFUnits.kVoltage,
    )

  def stop(self):
    self.elevatorMotor.set(0)
