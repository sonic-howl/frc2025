from commands2 import Command


class TestCommand(Command):
  def __init__(self, drivetrain) -> None:
    super().__init__()
    self.drivetrain = drivetrain
    self.addRequirements(drivetrain)

  def initialize(self) -> None:
    """Called when the command is initially scheduled."""

  def execute(self) -> None:
    """Called every time the scheduler runs while the command is scheduled."""

  def end(self, interrupted: bool) -> None:
    """Called once the command ends or is interrupted."""

  def isFinished(self) -> bool:
    """Returns true when the command should end."""
