import webview
import os
import signal
from pathlib import Path
from api import API

ENV = os.getenv("APP_ENV", "production")
BASE_DIR = Path(__file__).resolve().parent

def run_app():
    api = API()
    
    # differentiate dev/prod urls
    if ENV == "development":
        url = "http://localhost:5173"
        print(f"Development mode: Using URL: {url}")
    else:
        url = str(BASE_DIR / "build" / "index.html")
        print("Production mode: Using local build")

    # force ctrl+c
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # start webview
    window = webview.create_window("BlobSculptor", url, js_api=api)
    webview.start(http_server=(ENV != "development"), debug=True)

if __name__ == "__main__":
    run_app()