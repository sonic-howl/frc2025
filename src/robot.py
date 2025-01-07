import wpilib
import wpilib.drive
from commands2 import CommandScheduler

from RobotContainer import RobotContainer
from Shuffleboard import addDeployArtifacts


class MyRobot(wpilib.TimedRobot):
  m_robotContainer: RobotContainer

  def __init__(self):
    super().__init__()
    self.m_robotContainer = RobotContainer()

  def robotInit(self):
    """
    This function is called upon program startup and
    should be used for any initialization code.
    """
    addDeployArtifacts()

  def robotPeriodic(self):
    """This function is called periodically every ~20ms."""
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
    CommandScheduler.getInstance().cancelAll()

  def testPeriodic(self):
    """This function is called periodically during test mode."""


if __name__ == "__main__":
  wpilib.run(MyRobot)
