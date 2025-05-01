from playwright.async_api import async_playwright
import asyncio

async def main():
  async with async_playwright() as pw:
        # Kết nối trực tiếp qua port được exposed ra ngoài
        browser = await pw.chromium.connect_over_cdp("http://localhost:3000")
        # Hoặc nếu không hoạt động, thử sử dụng
        # browser = await pw.chromium.connect_over_cdp("http://localhost:3000")
        
        # Nếu không tự động nhận được contexts, tạo mới 
        if len(browser.contexts) == 0:
            ctx = await browser.new_context()
            page = await ctx.new_page()
        else:
            ctx = browser.contexts[0]
            if len(ctx.pages) == 0:
                page = await ctx.new_page()
            else:
                page = ctx.pages[0]
        
        print("Page URL:", page.url)
        await page.goto("https://google.com")
        print("New Page URL:", page.url)
    
if __name__ == "__main__":
    asyncio.run(main())