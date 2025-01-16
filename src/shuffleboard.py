import ntcore
import wpilib
from commands2 import Command, Subsystem
from wpilib.shuffleboard import BuiltInLayouts, Shuffleboard


class ShuffleboardTabs:
  kCommandBotTab = "CommandBot"
  kMetadataTab = "metadata"


def addDeployArtifacts():
  if wpilib.RobotBase.isReal():  # getDeployData() returns None during simulation
    deployArtifacts = wpilib.deployinfo.getDeployData()
    (
      buildArtifactsLayout := Shuffleboard.getTab(ShuffleboardTabs.kMetadataTab)
      .getLayout("DeployArtifacts", BuiltInLayouts.kList)
      .withSize(3, 2)
      .withProperties({"Label position": ntcore._ntcore.Value.makeString("LEFT")})
    )

    buildArtifactsLayout.add("GIT_BRANCH", deployArtifacts["git-branch"])
    buildArtifactsLayout.add("DEPLOY_DATE", deployArtifacts["deploy-date"])
    buildArtifactsLayout.add(
      "Uncommited Changes",
      "Yes" if "dirty" in deployArtifacts["git-desc"].split("-") else "No",
    )


def displaySubsystemStatus(subsystems: list[Subsystem]):
  commandBotTab = Shuffleboard.getTab(ShuffleboardTabs.kCommandBotTab)
  for subsystem in subsystems:
    subsystemLayout = commandBotTab.getLayout("Subsystems", BuiltInLayouts.kList)
    # TODO: See which add parameter is better
    subsystemLayout.add(subsystem.__class__.__name__, subsystem)
    subsystemLayout.add(subsystem)


def displayCommands(commands: list[Command]):
  commandBotTab = Shuffleboard.getTab(ShuffleboardTabs.kCommandBotTab)
  for command in commands:
    commandLayout = commandBotTab.getLayout("Commands", BuiltInLayouts.kList)
    # TODO: See which add parameter is better
    commandLayout.add(command.getName(), command)
    commandLayout.add(command)
