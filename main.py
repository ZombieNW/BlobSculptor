import webview
import os
import sys
import signal
from pathlib import Path
from api import API

ENV = os.getenv("APP_ENV", "production")

# Helper to get resources depending on environment
def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def run_app():
    api = API()
    
    # differentiate dev/prod urls
    if ENV == "development":
        url = "http://localhost:5173"
        print(f"Development mode: Using URL: {url}")
    else:
        build_dir = get_resource_path("build")
        url = os.path.join(build_dir, "index.html")
        print(f"Production mode: Using URL: {url}")

    # force ctrl+c
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # start webview
    window = webview.create_window("BlobSculptor", url, js_api=api)
    api.set_window(window) # set window in api
    webview.start(http_server=(ENV != "development"), debug=(ENV == "development"))

if __name__ == "__main__":
    run_app()