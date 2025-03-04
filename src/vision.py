# NOTE: This code runs in its own process, so we cannot access the robot here,
#       nor can we create/use/see wpilib objects
#
# To try this code out locally (if you have robotpy-cscore installed), you
# can execute `python3 -m cscore vision.py:main`

from cscore import CameraServer as CS


# Example code taken from: https://docs.wpilib.org/en/stable/docs/software/vision-processing/roborio/using-the-cameraserver-on-the-roborio.html
def main():
  CS.enableLogging()

  # Get the UsbCamera from CameraServer
  camera = CS.startAutomaticCapture()
  camera.setResolution(640, 480)
  # camera.setFPS(30)

  # camera.setExposureAuto()
  # camera.setWhiteBalanceAuto()
  # camera.setExposureManual()
  # camera.setBrightness()
