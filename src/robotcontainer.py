import wpilib
from commands2 import Command, cmd
from commands2.button import CommandXboxController
from wpilib import SmartDashboard

from constants import ControllerConstants
from subsystems import DriveSubsystem


class RobotContainer:
  """
  This class is where the bulk of the robot should be declared. Since Command-based is a
  "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
  periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
  subsystems, commands, and button mappings) should be declared here.
  """

  def __init__(self) -> None:
    # Initialise the robot's subsystems
    self.robotDrive = DriveSubsystem()

    # Initialize the controllers
    self.driverController = CommandXboxController(
      ControllerConstants.kDriverControllerPort
    )
    self.operatorController = CommandXboxController(
      ControllerConstants.kOperatorControllerPort
    )
    self.configureButtonBindings()

    self.configureAuto()

  def configureButtonBindings(self):
    # Note: Trigger objects do not need to survive past the call to a binding method.
    xButton = self.driverController.x()
    xButton.onTrue(cmd.runOnce(lambda: print("x Button Pressed")))

    yButton = self.driverController.y()
    yButton.debounce().whileTrue(cmd.run(lambda: print("y Button Held")))

  def configureAuto(self):
    self.autoSelector = wpilib.SendableChooser()
    self.autoSelector.setDefaultOption(
      "Default Option (Test)", cmd.runOnce(lambda: print("Default Autonomous Command"))
    )
    self.autoSelector.addOption(
      "Test Option", cmd.runOnce(lambda: print("Test Autonomous Command"))
    )
    SmartDashboard.putData(self.autoSelector)

  def getAutonomousCommand(self) -> Command:
    """
    Get the command to run in autonomous
    """
    return self.autoSelector.getSelected()

  # Might not be needed if using command buttons on the shuffleboard
  def getTestCommand(self) -> Command:
    """
    Get the command to run in test mode
    """
    return None
