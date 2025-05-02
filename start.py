import os
import subprocess
from gologin.gologin import GoLogin
from playwright.async_api import async_playwright
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from io import BytesIO


def start_browser():
    PROFILE_ID = "67eeb053a9cb6a7191579b8b"
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2VlYWJmOGJkODY2YjdjM2Y2NmIzZjEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2VlYWMyNjcwZTM0MDBhNWY2YjdkZmUifQ.tUvpgtJL0swAUinAx1XIeWt4OQMjBqszIciDPKoE9Nk"
    DISPLAY = ":99"

    param = [
        "/usr/bin/orbita-browser/chrome",
        "--remote-debugging-port=3500",
        "--user-data-dir=/tmp/gologin_67eeb053a9cb6a7191579b8b",
        "--password-store=basic",
        "--gologin-profile=linux",
        "--lang=en-US",
        "--disable-gpu",
        "--webrtc-ip-handling-policy=default_public_interface_only",
        "--disable-features=PrintCompositorLPAC",
        "--remote-debugging-address=0.0.0.0",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--window-size=1920,1080",
        "--disable-software-rasterizer",
    ]
    exts = load_extension("extension")
    param.extend(exts)
    subprocess.Popen(param, start_new_session=True)


def load_extension(dir):
    cmd = (
        f"for f in {dir}/*.zip;"
        + ' do unzip -qo "$f" -d  "${f%.*}"; done '
        + f"&& ls -d {dir}/*/"
    )
    exts = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
    return [f"--load-extension={ext}" for ext in exts.stdout.strip().split("\n")]


if __name__ == "__main__":
    start_browser()
