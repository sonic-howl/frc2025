import typing

import wpilib
import wpilib.drive
from commands2 import Command, CommandScheduler, TimedCommandRobot
from wpilib import SmartDashboard

from robotcontainer import RobotContainer
from shuffleboard import addDeployArtifacts
from subsystems.SwerveModule import SwerveModule


class MyRobot(TimedCommandRobot):
  autonomousCommand: typing.Optional[Command] = None

  def robotInit(self):
    """
    This function is called upon program startup and
    should be used for any initialization code.
    """
    addDeployArtifacts()

    self.robotContainer = RobotContainer()
    self.swerveModule = SwerveModule()

  def robotPeriodic(self):
    CommandScheduler.getInstance().run()
    SmartDashboard.putString(
      "Front Left (Bot Oriented)",
      f"{self.robotContainer.driveSubsystem.frontLeft.getPosition().angle.degrees}",
    )
    SmartDashboard.putString(
      "Front Right (Bot Oriented)",
      f"{self.robotContainer.driveSubsystem.frontRight.getPosition().angle.degrees}",
    )
    SmartDashboard.putString(
      "Back Left (Bot Oriented)",
      f"{self.robotContainer.driveSubsystem.backLeft.getPosition().angle.degrees}",
    )
    SmartDashboard.putString(
      "Back Right (Bot Oriented)",
      f"{self.robotContainer.driveSubsystem.backRight.getPosition().angle.degrees}",
    )
    SmartDashboard.putString(
      "Front Left (Bot Oriented - Drive Motor)",
      f"{self.swerveModule.driveMotor.get_position}",
    )

  def autonomousInit(self):
    """This function is run once each time the robot enters autonomous mode."""

    self.autonomousCommand = self.robotContainer.getAutonomousCommand()

    if self.autonomousCommand:
      self.autonomousCommand.schedule()

  def autonomousPeriodic(self):
    """This function is called periodically during autonomous."""

  def teleopInit(self):
    """This function is called once each time the robot enters teleoperated mode."""

    if self.autonomousCommand:
      self.autonomousCommand.cancel()

  def teleopPeriodic(self):
    """This function is called periodically during teleoperated mode."""

  def testInit(self):
    """This function is called once each time the robot enters test mode."""

  def testPeriodic(self):
    """This function is called periodically during test mode."""


if __name__ == "__main__":
  wpilib.run(MyRobot)
