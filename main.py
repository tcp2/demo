import asyncio
import os
import subprocess
from typing import AsyncIterator
from gologin.gologin import GoLogin
from playwright.async_api import async_playwright
from fastapi import FastAPI
import logging
from fastapi.responses import StreamingResponse
from io import BytesIO
from playwright.async_api import Browser, Page
from contextlib import asynccontextmanager

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
                "--remote-debugging-address=0.0.0.0--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--window-size=1920,1080",
                "--disable-software-rasterizer",
            ],
        }
    )
    gl.start()
    return {"status": "ok"}


@asynccontextmanager
async def getPage() -> AsyncIterator[Page]:
    async with async_playwright() as pw:
        try:
            browser = await pw.chromium.connect_over_cdp("http://localhost:3500")
            ctx = browser.contexts[0]
            p = await ctx.new_page()
            try:
                yield p
            finally:
                await p.close()
        except Exception as e:
            logging.error(e)
            raise

        finally:
            if "p" in locals() and not p.is_closed():
                await p.close()


@app.get("/api/screenshot")
async def screenshot():
    async with getPage() as p:
        await p.goto("https://example.com")
        logging.info("Page URL: %s", p.url)

        ("Page URL:", p.url)
        await p.wait_for_timeout(2000)
        buf = await p.screenshot()

    return StreamingResponse(BytesIO(buf), media_type="image/png")


@app.get("/api/automa")
async def runAutoma():
    async with getPage() as p:
        await p.goto(
            "chrome-extension://ebnjojalilbeniejjakdeilkiejcjhep/execute.html#/7dmgX875oL49qe11GVfTk"
        )
        await asyncio.sleep(5)
        
        buf = await p.screenshot()
        return StreamingResponse(BytesIO(buf), media_type="image/png")


@app.get("/stopall")
async def stop_all():
    subprocess.run(["pkill", "Xvfb"])
    subprocess.run(["pkill", "chrome"])
    return {"status": "ok"}


if __name__ == "__main__":
    start()
