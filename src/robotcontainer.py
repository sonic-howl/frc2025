import wpilib
from commands2 import Command, cmd
from commands2.button import CommandXboxController
from wpilib import SmartDashboard

from constants import ControllerConstants


class RobotContainer:
  def __init__(self):
    self.driverController = CommandXboxController(
      ControllerConstants.kDriverControllerPort
    )
    self.operatorController = CommandXboxController(
      ControllerConstants.kOperatorControllerPort
    )

    self.configureButtonBindings()
    self.configureAuto()

  def configureButtonBindings(self):
    self.driverXButton = self.driverController.x()
    self.driverXButton.onTrue(cmd.runOnce(lambda: print("X Button Pressed (Driver)")))

    self.operatorYButton = self.operatorController.y()
    self.operatorYButton.whileTrue(
      cmd.runOnce(lambda: print("Y Button Pressed (Operator)"))
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
