import wpilib
import wpimath
from commands2 import Command, RunCommand, cmd
from commands2.button import CommandXboxController
from wpilib import SmartDashboard
from wpilib.cameraserver import CameraServer

from constants import (
  DriverControllerConstants,
  ElevatorSubsystemConstants,
  OperatorControllerConstants,
)
from subsystems.DriveSubsystem import DriveSubsystem
from subsystems.ElevatorSubsystem import ElevatorSubsystem
from subsystems.PickupSubsystem import PickupSubsystem


class RobotContainer:
  def __init__(self):
    # Note: Vision processing shouldn't be run in the robot code. It should be run in a separate process (vision.py).
    CameraServer.launch("vision.py:main")

    self.driveSubsystem = DriveSubsystem()
    self.elevatorSubsystem = ElevatorSubsystem()
    self.pickupSubsystem = PickupSubsystem()

    self.driverController = CommandXboxController(DriverControllerConstants.kDriverControllerPort)
    self.operatorController = CommandXboxController(
      OperatorControllerConstants.kOperatorControllerPort
    )

    self.configureButtonBindings()
    self.configureAuto()

    self.fieldRelative = False

    self.driveSubsystem.setDefaultCommand(
      RunCommand(
        lambda: self.driveSubsystem.drive(
          wpimath.applyDeadband(
            -self.driverController.getLeftY(), DriverControllerConstants.kDriveDeadband
          ),
          wpimath.applyDeadband(
            -self.driverController.getLeftX(), DriverControllerConstants.kDriveDeadband
          ),
          wpimath.applyDeadband(
            -self.driverController.getRightX(), DriverControllerConstants.kDriveDeadband
          ),
          self.fieldRelative,
        ),
        self.driveSubsystem,
      )
    )

    self.elevatorSubsystem.setDefaultCommand(
      RunCommand(lambda: self.elevatorSubsystem.stop(), self.elevatorSubsystem)
    )
    self.pickupSubsystem.setDefaultCommand(
      RunCommand(lambda: self.pickupSubsystem.stop(), self.pickupSubsystem)
    )

  def teleopPeriodic(self):
    ### Manual Elevator Commands ###
    y = wpimath.applyDeadband(
      self.operatorController.getLeftY(), OperatorControllerConstants.kElevateDeadband
    )
    if abs(y) > 0:
      elevatorCurrentCommand = self.elevatorSubsystem.getCurrentCommand()
      if elevatorCurrentCommand is not None:
        elevatorCurrentCommand.cancel()
      self.elevatorSubsystem.manualDrive(-y)

    ### Manual Pickup Commands ###
    leftTriggerAxis = wpimath.applyDeadband(
      self.operatorController.getLeftTriggerAxis, OperatorControllerConstants.kPickupDeadband
    )
    rightTriggerAxis = wpimath.applyDeadband(
      self.operatorController.getRightTriggerAxis, OperatorControllerConstants.kPickupDeadband
    )

    pickupCurrentCommand = self.pickupSubsystem.getCurrentCommand()
    if pickupCurrentCommand is not None:
      pickupCurrentCommand.cancel()

    if leftTriggerAxis > 0:
      self.pickupSubsystem.manualDrive(leftTriggerAxis)
    elif rightTriggerAxis > 0:
      self.pickupSubsystem.manualDrive(-rightTriggerAxis)

  def configureButtonBindings(self):
    """
    Configures button functions for both the Driver and Operator XBox Controllers.
    """
    ### Driver Controller ###
    self.driverController.x().whileTrue(
      cmd.run(lambda: self.driveSubsystem.setX, self.driveSubsystem)
    )

    ### Operator Controller ###
    self.operatorController.y().onTrue(RunCommand(lambda: self.elevatorSubsystem.zeroPosition()))

    self.operatorController.povUp().onTrue(
      cmd.runOnce(
        lambda: self.elevatorSubsystem.goToPosition(ElevatorSubsystemConstants.kMiddleSetPoint),
        self.elevatorSubsystem,
      )
    )
    self.operatorController.povRight().onTrue(
      cmd.runOnce(
        lambda: self.elevatorSubsystem.goToPosition(ElevatorSubsystemConstants.kBottomSetPoint),
        self.elevatorSubsystem,
      )
    )
    self.operatorController.povDown().onTrue(
      cmd.runOnce(
        lambda: self.elevatorSubsystem.goToPosition(ElevatorSubsystemConstants.kScoreSetPoint),
        self.elevatorSubsystem,
      )
    )

  def configureAuto(self):
    self.autoSelector = wpilib.SendableChooser()
    self.autoSelector.setDefaultOption(
      "Default Option (test)",
      cmd.runOnce(lambda: print("Default Autonomous Command")),
    )
    self.autoSelector.addOption(
      "Test Option", cmd.runOnce(lambda: print("Test Autonomous Command"))
    )
    SmartDashboard.putData("AutoSelector", self.autoSelector)

  def getAutonomousCommand(self) -> Command:
    return self.autoSelector.getSelected()
