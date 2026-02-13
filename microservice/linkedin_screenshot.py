from seleniumbase import SB
import os
import time

def parse_netscape_cookies(cookie_file):
    cookies = []
    with open(cookie_file, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue

            parts = line.strip().split('\t')
            if len(parts) >= 7:
                domain = parts[0]

                # Filter for LinkedIn domain to speed up
                if 'linkedin' not in domain:
                    continue

                # flag = parts[1] # Not usually needed for selenium dict
                path = parts[2]
                secure = parts[3].upper() == 'TRUE'
                expires = int(parts[4]) if parts[4].isdigit() and int(parts[4]) > 0 else None
                name = parts[5]
                value = parts[6]

                cookie = {
                    'name': name,
                    'value': value,
                    'domain': domain,
                    'path': path,
                    'secure': secure
                }
                if expires:
                    cookie['expiry'] = expires

                cookies.append(cookie)
    return cookies

def screenshot_linkedin():
    # Path to cookies file
    cookies_file = os.path.abspath("cookies/linkedin.txt")
    screenshot_path = os.path.abspath("linkedin_jobs.png")

    print(f"Using cookies from: {cookies_file}")

    if not os.path.exists(cookies_file):
        print(f"Error: Cookie file not found at {cookies_file}")
        return

    netscape_cookies = parse_netscape_cookies(cookies_file)
    print(f"Parsed {len(netscape_cookies)} LinkedIn cookies.")

    if not netscape_cookies:
        print("No LinkedIn cookies found.")
        return

    with SB(uc=True, test=True, headless=False, headed=True) as sb:
        # 1. Open LinkedIn domain first to set cookies context
        print("Opening LinkedIn...")
        sb.open("https://www.linkedin.com")

        # 2. Load cookies manually
        print("Adding cookies...")
        for cookie in netscape_cookies:
            try:
                sb.driver.add_cookie(cookie)
            except Exception as e:
                # Ignore specific cookie errors
                pass

        # 3. Navigate to Jobs page
        print("Navigating to Jobs page...")
        sb.open("https://www.linkedin.com/jobs/")

        # 4. Wait for page to load
        try:
            sb.wait_for_element("div.application-outlet", timeout=10)
            print("Jobs page loaded.")
        except Exception:
            print("Timeout waiting for specific element, proceeding to screenshot anyway.")

        # 5. Take screenshot
        print(f"Taking screenshot to {screenshot_path}...")
        sb.save_screenshot(screenshot_path)
        print("Screenshot saved.")

if __name__ == "__main__":
    screenshot_linkedin()
