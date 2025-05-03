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

app = FastAPI()

os.environ["DISPLAY"] = DISPLAY

@app.get("/api/ping")
def ping():
    return {"status": "ok"}

@app.get("/api/start")
def start():
    gl = GoLogin(
        {
            "headless": False,
            "executablePath": "/usr/bin/orbita-browser/chrome",
            "token": TOKEN,
            "profile_id": PROFILE_ID,
            "credentials_enable_service": False,
            "port": 3500,
            "extra_params": [
                "--remote-debugging-address=0.0.0.0"
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--window-size=1920,1080",
                "--disable-software-rasterizer",
            ],
        }
    )
    gl.start()
    return {"status": "ok"}


@app.get("/api/screenshot")
async def screenshot():
    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp("http://localhost:3500")
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        print("Page URL:", page.url)
        await page.goto("https://example.com")
        await page.wait_for_timeout(2000)
        buf = await page.screenshot()
        return StreamingResponse(BytesIO(buf), media_type="image/png")


@app.get("/api/automa")
async def runAutoma():
    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp("http://localhost:3500")
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        print("Page URL:", page.url)
        await page.goto("chrome-extension://ebnjojalilbeniejjakdeilkiejcjhep/execute.html#/7dmgX875oL49qe11GVfTk")
        await page.wait_for_timeout(2000)
        buf = await page.screenshot()
        return StreamingResponse(BytesIO(buf), media_type="image/png")


@app.get("/stopall")
async def stop_all():
    subprocess.run(["pkill", "Xvfb"])
    subprocess.run(["pkill", "chrome"])
    return {"status": "ok"}


if __name__ == "__main__":
    start()
