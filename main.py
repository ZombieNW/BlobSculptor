import webview
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INDEX_HTML = str(BASE_DIR / "build" / "index.html")

if __name__ == "__main__":
    window = webview.create_window("BlobSculptor", INDEX_HTML)
    webview.start(http_server=True, debug=True)