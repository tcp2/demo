import os
import subprocess
from gologin.gologin import GoLogin
from playwright.async_api import async_playwright
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from io import BytesIO

PROFILE_ID = "67eeb053a9cb6a7191579b8b"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2VlYWJmOGJkODY2YjdjM2Y2NmIzZjEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2N2VlYWMyNjcwZTM0MDBhNWY2YjdkZmUifQ.tUvpgtJL0swAUinAx1XIeWt4OQMjBqszIciDPKoE9Nk"
DISPLAY = ":99"

gl = GoLogin(
    {
        "headless": False,
        "executablePath": "/usr/bin/orbita-browser/chrome",
        "token": TOKEN,
        "profile_id": PROFILE_ID,
        "credentials_enable_service": False,
        "port": 3500,
        "extra_params": [
            "--remote-debugging-address=0.0.0.0",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--window-size=1920,1080",
            "--disable-software-rasterizer",
        ],
    }
)
gl.start()
