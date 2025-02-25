import wpilib
import wpimath
from commands2 import Command, RunCommand, cmd
from commands2.button import CommandXboxController
from wpilib import SmartDashboard
from wpimath.geometry import Rotation2d
from wpimath.kinematics import (
  SwerveModuleState,
)

from constants import ControllerConstants
from subsystems.DriveSubsystem import DriveSubsystem


class RobotContainer:
  def __init__(self):
    self.driveSubsystem = DriveSubsystem()

    self.driverController = CommandXboxController(
      ControllerConstants.kDriverControllerPort
    )
    # self.operatorController = CommandXboxController(
    #   ControllerConstants.kOperatorControllerPort
    # )

    self.configureButtonBindings()
    self.configureAuto()

    self.fieldRelative = True

    self.driveSubsystem.setDefaultCommand(
      RunCommand(
        lambda: self.driveSubsystem.drive(
          wpimath.applyDeadband(
            self.driverController.getLeftX(), ControllerConstants.kDriveDeadband
          ),
          wpimath.applyDeadband(
            self.driverController.getLeftY(), ControllerConstants.kDriveDeadband
          ),
          wpimath.applyDeadband(
            self.driverController.getRightX(), ControllerConstants.kDriveDeadband
          ),
          self.fieldRelative,
        ),
        self.driveSubsystem,
      )
    )

  def configureButtonBindings(self):
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
        lambda: self.driveSubsystem.frontLeft.setDesiredState(
          SwerveModuleState(1, Rotation2d.fromDegrees(90))
        ),
        self.driveSubsystem,
      )
    )

  def configureAuto(self):
    self.autoSelector = wpilib.SendableChooser()
    self.autoSelector.setDefaultOption(
      "Default Option (test)", cmd.runOnce(lambda: print("Default Autonomous Command"))
    )
    self.autoSelector.addOption(
      "Test Option", cmd.runOnce(lambda: print("Test Autonomous Command"))
    )
    SmartDashboard.putData("AutoSelector", self.autoSelector)

  def getAutonomousCommand(self) -> Command:
    return self.autoSelector.getSelected()
