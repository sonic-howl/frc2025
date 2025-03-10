import wpilib
import wpimath
from commands2 import Command, RunCommand, cmd
from commands2.button import CommandXboxController
from pathplannerlib.auto import AutoBuilder, NamedCommands
from pathplannerlib.events import EventTrigger
from wpilib import Field2d, SmartDashboard

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
    self.field = Field2d()
    SmartDashboard.putData("Field", self.field)

    self.driveSubsystem = DriveSubsystem()
    self.elevatorSubsystem = ElevatorSubsystem()
    self.pickupSubsystem = PickupSubsystem()

    self.driverController = CommandXboxController(DriverControllerConstants.kDriverControllerPort)
    self.operatorController = CommandXboxController(
      OperatorControllerConstants.kOperatorControllerPort
    )

    self.configureButtonBindings()
    self.configureAuto()

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
          DriveSubsystem.fieldRelative,
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
      self.operatorController.getLeftTriggerAxis(), OperatorControllerConstants.kPickupDeadband
    )
    rightTriggerAxis = wpimath.applyDeadband(
      self.operatorController.getRightTriggerAxis(), OperatorControllerConstants.kPickupDeadband
    )

    pickupCurrentCommand = self.pickupSubsystem.getCurrentCommand()
    if pickupCurrentCommand is not None:
      pickupCurrentCommand.cancel()

    if leftTriggerAxis > 0:
      self.pickupSubsystem.manualDrive(leftTriggerAxis)
    elif rightTriggerAxis > 0:
      self.pickupSubsystem.manualDrive(-rightTriggerAxis)

    ### Shuffleboard ###
    self.field.setRobotPose(self.driveSubsystem.getPose())
    SmartDashboard.putBoolean("Field Relative", DriveSubsystem.fieldRelative)

  def configureButtonBindings(self):
    """
    Configures button functions for both the Driver and Operator XBox Controllers.
    """
    ### Driver Controller ###
    self.driverController.x().whileTrue(
      cmd.run(lambda: self.driveSubsystem.setX, self.driveSubsystem)
    )

    self.driverController.back().onTrue(
      cmd.runOnce(lambda: self.driveSubsystem.toggleFieldRelative())
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
    self.configureNamedCommands()
    self.configureTriggerCommands()
    # Build an auto chooser. This will use Commands.none() as the default option.
    # Another option that allows you to specify the default auto by its name
    self.autoChooser = AutoBuilder.buildAutoChooser()

    SmartDashboard.putData("Auto Chooser", self.autoChooser)

  def configureNamedCommands(self):
    # Commands need
    NamedCommands.registerCommand("printHello", cmd.runOnce(lambda: print("Hello")))

  def configureTriggerCommands(self):
    # More info on Command Triggers here: https://pathplanner.dev/pplib-triggers.html
    # EventTrigger("runIntake").whileTrue(cmd.print("running intake"))
    pass

  def getAutonomousCommand(self) -> Command:
    return self.autoChooser.getSelected()
