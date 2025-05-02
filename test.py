from playwright.async_api import async_playwright
import asyncio

import requests


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp("http://m1.laobo.xyz")
        wk_id = '7dmgX875oL49qe11GVfTk'
        url = f'chrome-extension://ebnjojalilbeniejjakdeilkiejcjhep/execute.html#/{wk_id}'
        # await p.goto("chrome::/")
        # print("New p URL:", p.url)
        # 


if __name__ == "__main__":
    asyncio.run(main())
