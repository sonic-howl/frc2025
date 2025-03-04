import wpilib
import wpimath
from commands2 import Command, RunCommand, cmd
from commands2.button import CommandXboxController
from pathplannerlib.auto import AutoBuilder, NamedCommands
from wpilib import SmartDashboard

from constants import DriverControllerConstants, OperatorControllerConstants
from subsystems.DriveSubsystem import DriveSubsystem
from subsystems.ElevatorSubsystem import ElevatorSubsystem
from subsystems.PickupSubsystem import PickupSubsystem


class RobotContainer:
  def __init__(self):
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
      RunCommand(
        lambda: self.elevatorSubsystem.manualDrive(
          wpimath.applyDeadband(
            -(
              self.operatorController.getLeftY()
            ),  # Inverted because "up" on a joystick returns a negative value.
            OperatorControllerConstants.kElevateDeadband,
          )
        ),
        self.elevatorSubsystem,
      )
    )
    # self.elevatorSubsystem.setDefaultCommand(
    #   RunCommand(lambda: self.elevatorSubsystem.stop(), self.elevatorSubsystem)
    # )

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
    self.operatorController.leftBumper().whileTrue(RunCommand(lambda: self.pickupSubsystem.pull()))
    self.operatorController.rightBumper().whileTrue(RunCommand(lambda: self.pickupSubsystem.push()))
    self.operatorController.y().onTrue(RunCommand(lambda: self.elevatorSubsystem.zeroPosition()))

  def configureAuto(self):
    self.configureNamedCommands()

    # Build an auto chooser. This will use Commands.none() as the default option.
    # Another option that allows you to specify the default auto by its name
    self.autoChooser = AutoBuilder.buildAutoChooser()

    SmartDashboard.putData("Auto Chooser", self.autoChooser)

  def configureNamedCommands(self):
    # Commands need
    NamedCommands.registerCommand("printHello", cmd.runOnce(lambda: print("Hello")))

  def getAutonomousCommand(self) -> Command:
    return self.autoChooser.getSelected()
