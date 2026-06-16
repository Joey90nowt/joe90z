from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    console_messages = []
    page.on("console", lambda msg: console_messages.append({"type": msg.type, "text": msg.text}))
    page.on("pageerror", lambda err: console_messages.append({"type": "pageerror", "text": str(err)}))
    page.on("requestfailed", lambda req: console_messages.append({"type": "reqfail", "url": req.url, "failure": req.failure}))
    page.on("response", lambda resp: console_messages.append({"type": "resp", "url": resp.url, "status": resp.status, "headers": dict(resp.headers)}) if any(x in resp.url for x in ["mp3", "cover", "chapters"]) else None)

    page.goto('https://joey90nowt.github.io/joe90z/auto.html', timeout=15000)
    page.wait_for_timeout(10000)

    print("=== Relevant Responses ===")
    for m in console_messages:
        if m.get('type') == 'resp':
            print(json.dumps(m, indent=2))

    print("\n=== Errors/Failed ===")
    for m in console_messages:
        if m.get('type') in ('pageerror', 'reqfail', 'error'):
            print(json.dumps(m, indent=2))

    browser.close()