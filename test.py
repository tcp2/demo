from playwright.async_api import async_playwright
import asyncio

async def main():
  async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp("http://localhost:3000")
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        print("Page URL:", page.url)
        await page.goto("https://google.com.com")
    
if __name__ == "__main__":
    asyncio.run(main())