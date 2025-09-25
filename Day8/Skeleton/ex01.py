from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Step 1. Create a browser
    # Can use chromium/firefox/webkit
    browser = p.chromium.launch(headless=False)
    # `headless` is for specifically seeing what the code is doing

    # Step 2. Create a new BrowserContext
    context = browser.new_context()
    page = context.new_page()

    # Step 3. Open a page
    page.goto("https://reddit.com")
    print(page.title())

    browser.close()
