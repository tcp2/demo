from playwright.async_api import async_playwright
import asyncio

import requests
import websockets


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp("http://m1.laobo.xyz")
        ctx = browser.contexts[0]
        p = await ctx.new_page()

        print("p URL:", p.url)
        wk_id = '7dmgX875oL49qe11GVfTk'
        url = f'chrome-extension://ebnjojalilbeniejjakdeilkiejcjhep/execute.html#/{wk_id}'
        await p.goto(url)
        # await p.goto("chrome::/")
        # print("New p URL:", p.url)
        # 


async def connect_to_websocket():
    uri = "ws://m1.laobo.xyz/devtools/browser/cc57e7e1-9c10-4371-a002-e97ec971cf56"
    async with websockets.connect(uri) as websocket:
        # Gửi một tin nhắn (nếu cần)
        await websocket.send("Hello, WebSocket!")
        
        # Nhận phản hồi từ WebSocket
        response = await websocket.recv()
        print(response)

if __name__ == "__main__":
    asyncio.run(connect_to_websocket())
