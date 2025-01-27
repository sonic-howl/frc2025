import ntcore
import wpilib
from wpilib.shuffleboard import BuiltInLayouts, Shuffleboard


def addDeployArtifacts():
  if wpilib.RobotBase.isReal():  # getDeployData() returns None during simulation
    deployArtifacts = wpilib.deployinfo.getDeployData()
    (
      buildArtifacts_layout := Shuffleboard.getTab("metadata")
      .getLayout("DeployArtifacts", BuiltInLayouts.kList)
      .withSize(3, 2)
      .withProperties({"Label position": ntcore._ntcore.Value.makeString("LEFT")})
    )

    buildArtifacts_layout.add("GIT_BRANCH", deployArtifacts["git-branch"])
    buildArtifacts_layout.add("DEPLOY_DATE", deployArtifacts["deploy-date"])
    buildArtifacts_layout.add(
      "Uncommited Changes",
      "Yes" if "dirty" in deployArtifacts["git-desc"].split("-") else "No",
    )
