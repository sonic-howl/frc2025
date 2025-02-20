# To see messages from networktables, you must setup logging
import logging

import navx
import wpilib
import wpilib.drive
import wpimath
import wpimath.controller
import wpimath.filter

import constants
from subsystems import drivesubsystem

logging.basicConfig(level=logging.DEBUG)


class MyRobot(wpilib.TimedRobot):
  def robotInit(self) -> None:
    """Robot initialization function"""
    self.driverController = wpilib.XboxController(constants.kDriverControllerPort)
    self.swerve = drivesubsystem.DriveSubsystem()

    # Slew rate limiters to make joystick inputs more gentle; 1/3 sec from 0 to 1.
    self.xspeedLimiter = wpimath.filter.SlewRateLimiter(3)
    self.yspeedLimiter = wpimath.filter.SlewRateLimiter(3)
    self.rotLimiter = wpimath.filter.SlewRateLimiter(3)

  def autonomousInit(self) -> None:
    pass

  def autonomousPeriodic(self) -> None:
    pass

  def teleopInit(self) -> None:
    pass

  def teleopPeriodic(self) -> None:
    # Teleop periodic logic
    self.driveWithJoystick(True)

    # temporary feedback for testing
    wpilib.SmartDashboard.putNumber(
      "Driver Left X (xSpeed)", int(self.driverController.getLeftX())
    )
    wpilib.SmartDashboard.putNumber(
      "Driver Left Y (ySpeed)", int(self.driverController.getLeftY())
    )
    wpilib.SmartDashboard.putNumber(
      "Driver Right X (Rotation)", int(self.driverController.getRightX())
    )
    wpilib.SmartDashboard.putNumber(
      "Driver Right Y (unused)", int(self.driverController.getRightY())
    )

  def testPeriodic(self) -> None:
    pass

  def driveWithJoystick(self, fieldRelative: bool) -> None:
    # Get the x speed. We are inverting this because Xbox controllers return
    # negative values when we push forward.
    xSpeed = (
      -self.xspeedLimiter.calculate(
        wpimath.applyDeadband(self.driverController.getLeftY(), 0.08)
      )
      # * drivesubsystem.kMaxSpeed
    )

    # Get the y speed or sideways/strafe speed. We are inverting this because
    # we want a positive value when we pull to the left. Xbox controllers
    # return positive values when you pull to the right by default.
    ySpeed = (
      -self.yspeedLimiter.calculate(
        wpimath.applyDeadband(self.driverController.getLeftX(), 0.08)
      )
      # * drivesubsystem.kMaxSpeed
    )

    # Get the rate of angular rotation. We are inverting this because we want a
    # positive value when we pull to the left (remember, CCW is positive in
    # mathematics). Xbox controllers return positive values when you pull to
    # the right by default.
    rot = (
      -self.rotLimiter.calculate(
        wpimath.applyDeadband(self.driverController.getRightX(), 0.08)
      )
      # * drivesubsystem.kMaxSpeed
    )

    self.swerve.drive(xSpeed, ySpeed, rot, fieldRelative, rateLimit=True)


if __name__ == "__main__":
  wpilib.run(MyRobot)
