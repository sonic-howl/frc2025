import math

import wpilib
import wpimath.geometry
import wpimath.kinematics
from commands2 import Subsystem
from SwerveModule import SwerveModule

from constants import RobotConstants


class DriveSubsystem(Subsystem):
  def __init__(self) -> None:
    super().__init__()

    self.frontLeftLocation = RobotConstants.kFrontLeftLocation
    self.frontRightLocation = RobotConstants.kFrontRightLocation
    self.backLeftLocation = RobotConstants.kBackLeftLocation
    self.backRightLocation = RobotConstants.kBackRightLocation

    self.frontLeft = SwerveModule(1, 2, 0, 1, 2, 3)
    self.frontRight = SwerveModule(3, 4, 4, 5, 6, 7)
    self.backLeft = SwerveModule(5, 6, 8, 9, 10, 11)
    self.backRight = SwerveModule(7, 8, 12, 13, 14, 15)

    self.gyro = wpilib.AnalogGyro(0)
