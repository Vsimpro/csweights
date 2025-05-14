import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = None


def fetch_market_page( url: str, timing : int = 6, retries : int = 5  ) -> str:
    global driver
    global options

    site : str = ""

    if retries < 0:
        print( f"[!] Error in Steam. Repeat limit reached." )
        return ""

    try:

        if driver == None:
            driver = webdriver.Chrome(options=options)
        
        driver.get(url)
        time.sleep( timing )

        site = driver.page_source

        if "An error was encountered while processing your request".lower() in str(site).lower():
            print( f"[!] Error in Steam. Repeating in {timing*2}s .." )
            time.sleep( timing*2 )

            return fetch_market_page( url, timing, retries - 1 )

        time.sleep( timing*2 )

    except WebDriverException:
        print("[!] Error in connection")
        return ""

    return site
