from commands2.button import CommandXboxController

from constants import ControllerConstants


class RobotContainer:
  def __init__(self):
    self.driverController = CommandXboxController(
      ControllerConstants.kDriverControllerPort
    )

    self.configureButtonBindings()

  def configureButtonBindings(self):
    self.xButton = self.driverController.x()
    xButton.onTrue
