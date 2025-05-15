#
#   ChatGPT generated code
#

import asyncio
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def fetch_market_page(url: str, timing: int = 6, retries: int = 5) -> str:
    site: str = ""

    if retries < 0:
        print(f"[!] Error in Steam. Repeat limit reached.")
        return ""

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.goto(url, timeout=60000)  # 60s timeout
            page.wait_for_timeout(timing * 1000)  # Convert seconds to ms

            site = page.content()

            if "An error was encountered while processing your request" in site.lower():
                print(f"[!] Error in Steam. Repeating in {timing*2}s ..")
                page.wait_for_timeout(timing * 2000)
                browser.close()
                return fetch_market_page(url, timing, retries - 1)

            page.wait_for_timeout(timing * 2000)
            browser.close()

    except PlaywrightTimeoutError:
        print("[!] Timeout error during navigation.")
        return ""
    except Exception as e:
        print(f"[!] Error in connection: {e}")
        return ""

    return site