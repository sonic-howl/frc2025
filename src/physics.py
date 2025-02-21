from typing import TYPE_CHECKING

from pyfrc.physics.core import PhysicsEngine as Engine
from pyfrc.physics.core import PhysicsInterface
from wpilib.simulation import AnalogGyroSim
from wpimath.geometry import Pose2d, Rotation2d

if TYPE_CHECKING:
  from robot import MyRobot


class PhysicsEngine(Engine):
  simGyro = AnalogGyroSim(0)

  def __init__(self, physics_controller: PhysicsInterface, robot: "MyRobot"):
    """Initialize the physics engine with the simulation interface"""

    self.robot = robot
    self.physics_controller = physics_controller

    self.physics_controller.field.setRobotPose(Pose2d(5, 5, Rotation2d(0)))

  def update_sim(self, now: float, tm_diff: float):
    """Called when the simulation parameters for the program need to be updated"""

    """ swerveSubsystem = self.robot.robotContainer.swerveSubsystem

    if swerveSubsystem.swerveAutoStartPose:
      self.physics_controller.field.setRobotPose(swerveSubsystem.swerveAutoStartPose)
      swerveSubsystem.swerveAutoStartPose = None

    if swerveSubsystem.simChassisSpeeds:
      # the simulation turning is very slow, speed it up
      swerveSubsystem.simChassisSpeeds.omega *= 20
      pose = self.physics_controller.drive(swerveSubsystem.simChassisSpeeds, tm_diff)

      self.physics_controller.field.setRobotPose(pose)
      swerveSubsystem.resetOdometer(pose)

      self.simGyro.setAngle(pose.rotation().degrees()) """
    pass

    # swerveSubsystem = self.robot.swerve
    # pose = self.physics_controller.drive(swerveSubsystem.simChassisSpeeds, tm_diff)
