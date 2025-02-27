import wpilib
import wpimath
from commands2 import Command, RunCommand, cmd
from commands2.button import CommandXboxController
from wpilib import SmartDashboard

from constants import ControllerConstants
from subsystems.ActuatorSubsystems import ElevatorSubsystem, PickupSubsystem
from subsystems.DriveSubsystem import DriveSubsystem


class RobotContainer:
  def __init__(self):
    self.driveSubsystem = DriveSubsystem()
    self.elevatorSubstystem = ElevatorSubsystem()
    self.pickupSubsystem = PickupSubsystem()

    self.driverController = CommandXboxController(ControllerConstants.kDriverControllerPort)
    self.operatorController = CommandXboxController(ControllerConstants.kOperatorControllerPort)

    self.configureButtonBindings()
    self.configureAuto()

    self.fieldRelative = False

    self.driveSubsystem.setDefaultCommand(
      RunCommand(
        lambda: self.driveSubsystem.drive(
          wpimath.applyDeadband(self.driverController.getLeftX(), ControllerConstants.kDriveDeadband),
          wpimath.applyDeadband(-self.driverController.getLeftY(), ControllerConstants.kDriveDeadband),
          wpimath.applyDeadband(self.driverController.getRightX(), ControllerConstants.kDriveDeadband),
          self.fieldRelative,
        ),
        self.driveSubsystem,
      )
    )
    self.elevatorSubstystem.setDefaultCommand(RunCommand(lambda: self.elevatorSubstystem.stop(), self.elevatorSubstystem))
    self.pickupSubsystem.setDefaultCommand(RunCommand(lambda: self.pickupSubsystem.stop(), self.pickupSubsystem))
    # self.elevatorSubstystem.setDefaultCommand(RunCommand(lambda: self.elevatorSubstystem.elevate(wpimath.applyDeadband(self.operatorController.getRightY(), ControllerConstants.kElevateDeadband))))
    # self.pickupSubsystem.setDefaultCommand(RunCommand(lambda: self.pickupSubsystem.drive(self.operatorController.get)))

  def configureButtonBindings(self):
    """
    Configures button functions for both the Driver and Operator XBox Controllers.
    """

    # Examples
    # self.driverXButton = self.driverController.x()
    # self.driverXButton.onTrue(cmd.runOnce(lambda: print("X Button Pressed (Driver)")))

    # self.operatorYButton = self.operatorController.y()
    # self.operatorYButton.whileTrue(
    #   cmd.runOnce(lambda: print("Y Button Pressed (Operator)"))
    # )
    self.driverXButton = self.driverController.x()
    self.driverXButton.whileTrue(cmd.run(self.driveSubsystem.setX, self.driveSubsystem))

    self.driverYButton = self.driverController.y()
    self.driverYButton.whileTrue(
      cmd.run(
        self.driveSubsystem.setFrontLeft,
        self.driveSubsystem,
      )
    )
    self.operatorRightBumper = self.operatorController.rightBumper()
    self.operatorRightBumper.whileTrue(cmd.run(lambda: self.pickupSubsystem.drive()))
    self.operatorRightTrigger = self.operatorController.rightTrigger(0.2)
    self.operatorRightTrigger.whileTrue(cmd.run(lambda: self.pickupSubsystem.drive(True)))

    self.operatorLeftBumper = self.operatorController.leftBumper()
    self.operatorLeftBumper.whileTrue(cmd.run(lambda: self.elevatorSubstystem.drive()))
    self.operatorLeftTrigger = self.operatorController.leftTrigger(0.2)
    self.operatorLeftTrigger.whileTrue(cmd.run(lambda: self.elevatorSubstystem.drive(True)))

  def configureAuto(self):
    self.autoSelector = wpilib.SendableChooser()
    self.autoSelector.setDefaultOption("Default Option (test)", cmd.runOnce(lambda: print("Default Autonomous Command")))
    self.autoSelector.addOption("Test Option", cmd.runOnce(lambda: print("Test Autonomous Command")))
    SmartDashboard.putData("AutoSelector", self.autoSelector)

  def getAutonomousCommand(self) -> Command:
    return self.autoSelector.getSelected()
