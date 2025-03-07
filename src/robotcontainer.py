import math

import wpilib
import wpimath
from commands2 import Command, RunCommand, cmd
from commands2.button import CommandXboxController
from pathplannerlib.auto import AutoBuilder, NamedCommands
from pathplannerlib.events import EventTrigger
from wpilib import Field2d, SmartDashboard, Timer
from wpimath.filter import SlewRateLimiter

from constants import (
  DriverControllerConstants,
  ElevatorSubsystemConstants,
  OperatorControllerConstants,
  SwerveModuleConstants,
)
from subsystems.DriveSubsystem import DriveSubsystem
from subsystems.ElevatorSubsystem import ElevatorSubsystem
from subsystems.PickupSubsystem import PickupSubsystem


def sign(x: float):
  return 1 if x > 0 else -1


class RobotContainer:
  def __init__(self):
    self.field = Field2d()
    self.timer = Timer()

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
        lambda: self.drive(),
        self.driveSubsystem,
      )
    )

    # Slew rate limiters
    self.xLimiter = SlewRateLimiter(2)
    self.yLimiter = SlewRateLimiter(2)
    self.zLimiter = SlewRateLimiter(3)

    # self.elevatorSubsystem.setDefaultCommand(
    #   RunCommand(lambda: self.elevatorSubsystem.stop(), self.elevatorSubsystem)
    # )
    # self.pickupSubsystem.setDefaultCommand(
    #   RunCommand(lambda: self.pickupSubsystem.stop(), self.pickupSubsystem)
    # )

  def drive(self):
    square = 2.0 if SwerveModuleConstants.squareInputs else 1.0

    y = wpimath.applyDeadband(
      self.driverController.getLeftY(), DriverControllerConstants.kDriveDeadband
    )
    # y = self.yLimiter.calculate(y)
    y = -(y**square * sign(y))

    x = wpimath.applyDeadband(
      self.driverController.getLeftX(), DriverControllerConstants.kDriveDeadband
    )
    # x = self.xLimiter.calculate(x)
    x = -(x**square * sign(x))

    z = wpimath.applyDeadband(
      self.driverController.getRightX(), DriverControllerConstants.kDriveDeadband
    )
    # z = self.zLimiter.calculate(z)
    z = -(z**square * sign(z))

    self.driveSubsystem.drive(
      y,
      x,
      z,
      DriveSubsystem.fieldRelative,
    )

  def autonomousInit(self):
    # print("auto chosen", self.autoChooser.getSelected())
    self.timer.start()

  def teleopInit(self):
    self.timer.restart()

  def autonomousPeriodic(self):
    if not self.timer.hasElapsed(1):
      self.driveSubsystem.drive(0.75, 0, 0, False)
      # print("Driving")
    else:
      self.driveSubsystem.drive(0, 0, 0, False)
      # print("Stopped")

  def teleopPeriodic(self):
    ### Manual Elevator Commands ###
    y = wpimath.applyDeadband(
      -self.operatorController.getLeftY(), OperatorControllerConstants.kElevateDeadband
    )
    SmartDashboard.putNumber("Op. Left Y", abs(y))
    if abs(y) > 0:
      self.elevatorSubsystem.manualDrive(y)
    elif self.operatorController.povUp().getAsBoolean():
      self.elevatorSubsystem.goToPosition(ElevatorSubsystemConstants.kMiddleSetPoint)
    elif self.operatorController.povRight().getAsBoolean():
      self.elevatorSubsystem.goToPosition(ElevatorSubsystemConstants.kBottomSetPoint)
    elif self.operatorController.povDown().getAsBoolean():
      self.elevatorSubsystem.goToPosition(ElevatorSubsystemConstants.kScoreSetPoint)
    else:
      self.elevatorSubsystem.manualDrive(0)

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
      self.pickupSubsystem.manualDrive(-leftTriggerAxis)
    elif rightTriggerAxis > 0:
      self.pickupSubsystem.manualDrive(rightTriggerAxis)
    else:
      self.pickupSubsystem.stop()

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
    self.operatorController.y().onTrue(
      cmd.runOnce(lambda: self.elevatorSubsystem.zeroPosition(), self.elevatorSubsystem)
    )

    """ self.operatorController.povUp().whileTrue(
      cmd.run(
        lambda: self.elevatorSubsystem.goToPosition(ElevatorSubsystemConstants.kMiddleSetPoint),
        self.elevatorSubsystem,
      )
    )
    self.operatorController.povRight().whileTrue(
      cmd.run(
        lambda: self.elevatorSubsystem.goToPosition(ElevatorSubsystemConstants.kBottomSetPoint),
        self.elevatorSubsystem,
      )
    )
    self.operatorController.povDown().whileTrue(
      cmd.run(
        lambda: self.elevatorSubsystem.goToPosition(ElevatorSubsystemConstants.kScoreSetPoint),
        self.elevatorSubsystem,
      )
    ) """

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
