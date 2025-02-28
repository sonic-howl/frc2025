import wpilib
import wpimath
from commands2 import Command, RunCommand, cmd
from commands2.button import CommandXboxController
from wpilib import SmartDashboard

from constants import DriverControllerConstants, OperatorControllerConstants
from subsystems.DriveSubsystem import DriveSubsystem
from subsystems.ElevatorSubsystem import ElevatorSubsystem
from subsystems.PickupSubsystem import PickupSubsystem


class RobotContainer:
  def __init__(self):
    self.driveSubsystem = DriveSubsystem()

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

    self.elevatorSubstystem.setDefaultCommand(
      RunCommand(
        lambda: self.elevatorSubstystem.manualDrive(
          wpimath.applyDeadband(
            -(
              self.operatorController.getLeftY()
            ),  # Inverted because "up" on a joystick returns a negative value.
            OperatorControllerConstants.kElevateDeadband,
          )
        )
      )
    )

    self.pickupSubsystem.setDefaultCommand(RunCommand(lambda: self.pickupSubsystem.stop()))

  def configureButtonBindings(self):
    """
    Configures button functions for both the Driver and Operator XBox Controllers.
    """
    ### Driver Controller ###
    self.driverController.x().whileTrue(
      cmd.run(lambda: self.driveSubsystem.setX, self.driveSubsystem)
    )

    ### Operator Controller ###
    self.operatorController.leftBumper().whileTrue(cmd.run(lambda: self.pickupSubsystem.pull()))
    self.operatorController.rightBumper().whileTrue(cmd.run(lambda: self.pickupSubsystem.push()))

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
