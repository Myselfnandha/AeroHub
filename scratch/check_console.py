import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Listen for console logs and errors
        page.on("console", lambda msg: print(f"CONSOLE {msg.type.upper()}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err.message}"))
        
        print("Navigating to app URL...")
        await page.goto("http://127.0.0.1:8555/")
        
        # Wait for the app page to load
        await page.wait_for_timeout(3000)
        
        print("Navigating to Settings tab...")
        # Settings tab nav rail button (index 3)
        # Locate NavigationRail destinations
        try:
            settings_button = page.locator("text=Settings")
            await settings_button.click()
            await page.wait_for_timeout(2000)
        except Exception as e:
            print("Failed to click Settings:", e)
            
        print("Clicking Music Output Directory...")
        try:
            # Click on output directory textfield
            output_dir = page.get_by_label("Music Output Directory")
            await output_dir.click()
            await page.wait_for_timeout(2000)
        except Exception as e:
            print("Failed to click Music Output Directory:", e)
            
        print("Closing browser.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
