from base64 import b64decode
from pathlib import Path

from tethysapp.component_playground.app import App

downloads_folder = Path.home() / "Downloads"

@App.page
def webcam(lib):
    lib.register("webcam.js", "cam", host="/static/component_playground/js", default_export="WebCamera")
    return lib.tethys.Display(
        lib.cam.WebCamera(onCapture=lambda img: print("Captured image data:", img))
    )
