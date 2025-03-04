import math

from ntcore import NetworkTable, NetworkTableInstance
from wpimath.geometry import Pose2d, Rotation2d, Translation2d


class LimelightHelpers:
  def __init__(self):
    self.ll: NetworkTable = NetworkTableInstance.getDefault().getTable("limelight")
    self.poseTopic = self.ll.getDoubleArrayTopic("botpose_orb_wpiblue")

  @staticmethod
  def toPose2d(inData: list[float], timestamp: float) -> tuple[Pose2d, float]:
    """
    https://github.com/LimelightVision/limelight-examples/blob/28cb4c8f9b68cea62bef010ab793960f8d2b7a53/java-wpilib/swerve-aim-and-range/src/main/java/frc/robot/LimelightHelpers.java#L509

    public static Pose2d toPose2D(double[] inData){
      if(inData.length < 6)
      {
          //System.err.println("Bad LL 2D Pose Data!");
          return new Pose2d();
      }
      Translation2d tran2d = new Translation2d(inData[0], inData[1]);
      Rotation2d r2d = new Rotation2d(Units.degreesToRadians(inData[5]));
      return new Pose2d(tran2d, r2d);
    }
    """
    if len(inData) < 7:
      return (Pose2d(), 0.0)
    tran2d = Translation2d(inData[0], inData[1])
    r2d = Rotation2d(math.radians(inData[5]))
    totalLatency: float = inData[6]
    adjustedTimestamp = (timestamp / 1000000.0) - (totalLatency / 1000.0)
    return (Pose2d(tran2d, r2d), adjustedTimestamp)

  def getLLPose(self) -> tuple[Pose2d, float]:
    data = self.poseTopic.getEntry([]).getAtomic()
    pose = LimelightHelpers.toPose2d(data.value, data.time)
    return pose
