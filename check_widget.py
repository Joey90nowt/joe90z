from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    console_messages = []
    page.on("console", lambda msg: console_messages.append({"type": msg.type, "text": msg.text}))
    page.on("requestfailed", lambda req: console_messages.append({"type": "request_failed", "url": req.url, "failure": req.failure}))

    page.goto('http://146.103.58.195:8080', timeout=15000)
    page.wait_for_timeout(8000)

    print("=== Console Messages ===")
    for m in console_messages:
        print(json.dumps(m, indent=2))

    print("\n=== Page Text ===")
    print(page.inner_text('body'))

    browser.close()