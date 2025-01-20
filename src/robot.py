import wpilib
import wpilib.drive
from commands2 import CommandScheduler, TimedCommandRobot

from robotcontainer import RobotContainer
from shuffleboard import addDeployArtifacts


class MyRobot(TimedCommandRobot):
  def robotInit(self):
    """
    This function is called upon program startup and
    should be used for any initialization code.
    """
    addDeployArtifacts()

    self.robotContainer = RobotContainer()

  def robotPeriodic(self):
    CommandScheduler.getInstance().run()

  def autonomousInit(self):
    """This function is run once each time the robot enters autonomous mode."""

  def autonomousPeriodic(self):
    """This function is called periodically during autonomous."""

  def teleopInit(self):
    """This function is called once each time the robot enters teleoperated mode."""

  def teleopPeriodic(self):
    """This function is called periodically during teleoperated mode."""

  def testInit(self):
    """This function is called once each time the robot enters test mode."""

  def testPeriodic(self):
    """This function is called periodically during test mode."""


if __name__ == "__main__":
  wpilib.run(MyRobot)
