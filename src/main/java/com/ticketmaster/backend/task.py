#!/usr/bin/env python3
"""
TicketWatch backend watcher
Uses: undetected-chromedriver + mitmproxy

Usage: python task.py '<json_config>'
"""

import sys
import json
import time
import gzip
import signal
import smtplib
import traceback
import threading
import queue
from io import BytesIO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import bracex

# ── Brace expansion ────────────────────────────────────────────────────────

def _square_to_brace(s):
    stack = []
    s = list(s)
    for i, char in enumerate(s):
        if char == '[':
            stack.append(i)
        elif char == ']':
            start = stack.pop()
            s[start] = '{'
            s[i] = '}'
    return ''.join(s)

def expand_custom(s):
    converted = _square_to_brace(s)
    return list(bracex.expand(converted))


# ── SMTP Configuration ─────────────────────────────────────────────────────
SMTP_HOST     = "smtp.gmail.com"
SMTP_PORT     = 587
SMTP_USER     = "cdpl4ter@gmail.com"
SMTP_PASSWORD = "fwnb fqhs dxdz ovwm"

# ── Stdout helpers ─────────────────────────────────────────────────────────

def emit(obj: dict):
    print(json.dumps(obj, ensure_ascii=False), flush=True)

def log(text: str, level: str = "info"):
    emit({"type": "log", "text": text, "level": level})

def die(msg: str):
    emit({"type": "error", "text": msg})
    sys.exit(1)


# ── Mitmproxy addon ────────────────────────────────────────────────────────

class TicketmasterAddon:
    def __init__(self, data_queue: queue.Queue):
        self.q = data_queue

    def response(self, flow):
        url = flow.request.url
        is_facets = (
            "services.ticketmaster.ca/api/ismds/event" in url
            and "facets?by=section+seating" in url
        )
        is_offer = (
            ("offeradapter.ticketmaster.ca/api/ismds/event" in url
             or "services.ticketmaster.ca/api/ismds/event" in url)
            and "facets?apikey=" in url
        )
        if not (is_facets or is_offer):
            return
        if flow.request.method != "GET":
            return
        try:
            body = flow.response.content
            if not body:
                return
            stripped = body.lstrip()
            if not stripped.startswith(b"{") and not stripped.startswith(b"["):
                return
            enc = flow.response.headers.get("content-encoding", "")
            if "gzip" in enc:
                try:
                    with gzip.GzipFile(fileobj=BytesIO(body)) as f:
                        body = f.read()
                    stripped = body.lstrip()
                except Exception:
                    pass
            text = stripped.decode("utf-8").strip()
            if not text:
                return
            data = json.loads(text)
            self.q.put(("facets" if is_facets else "offer", data))
        except Exception:
            pass


def run_proxy(port: int, addon: TicketmasterAddon):
    import asyncio
    from mitmproxy.tools.dump import DumpMaster
    from mitmproxy.options import Options

    async def _run():
        opts = Options(listen_host="127.0.0.1", listen_port=port, ssl_insecure=True)
        master = DumpMaster(opts, with_termlog=False, with_dumper=False)
        master.addons.add(addon)
        await master.run()

    asyncio.run(_run())


# ── Chrome version detection ───────────────────────────────────────────────

def get_chrome_major_version() -> int:
    import subprocess, re
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in paths:
        try:
            out = subprocess.check_output([path, "--version"], stderr=subprocess.DEVNULL).decode()
            m = re.search(r"(\d+)\.\d+\.\d+", out)
            if m:
                return int(m.group(1))
        except Exception:
            pass
    return 145

# 别名供 task_debug.py 使用
get_chrome_major = get_chrome_major_version


# ── Pre-hider: suppress blank patch window ────────────────────────────────

def _start_prehider():
    if sys.platform != "win32":
        return lambda: None

    import ctypes
    import ctypes.wintypes

    _running = threading.Event()
    _running.set()
    user32 = ctypes.windll.user32
    EnumWindowsProc = ctypes.WINFUNCTYPE(
        ctypes.c_bool,
        ctypes.wintypes.HWND,
        ctypes.wintypes.LPARAM,
    )

    def cb(hwnd, _):
        cls_buf = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(hwnd, cls_buf, 256)
        if "Chrome" in cls_buf.value and user32.IsWindowVisible(hwnd):
            user32.ShowWindow(hwnd, 0)
        return True

    def loop():
        while _running.is_set():
            user32.EnumWindows(EnumWindowsProc(cb), 0)
            time.sleep(0.05)

    threading.Thread(target=loop, daemon=True).start()

    def stop():
        _running.clear()

    return stop


# ── Persistent window hider ───────────────────────────────────────────────

def start_window_hider(chrome_pid: int):
    if sys.platform != "win32":
        return
    import ctypes
    import ctypes.wintypes
    import subprocess as _sp

    user32 = ctypes.windll.user32
    EnumWindowsProc = ctypes.WINFUNCTYPE(
        ctypes.c_bool,
        ctypes.wintypes.HWND,
        ctypes.wintypes.LPARAM,
    )

    def get_tree(pid):
        pids = {pid}
        try:
            out = _sp.check_output(
                ["wmic", "process", "where",
                 f"ParentProcessId={pid}", "get", "ProcessId"],
                stderr=_sp.DEVNULL
            ).decode()
            for line in out.splitlines():
                line = line.strip()
                if line.isdigit():
                    pids |= get_tree(int(line))
        except Exception:
            pass
        return pids

    def hider():
        while True:
            try:
                pids = get_tree(chrome_pid)
                def cb(hwnd, _):
                    pid = ctypes.wintypes.DWORD()
                    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    if pid.value in pids and user32.IsWindowVisible(hwnd):
                        user32.ShowWindow(hwnd, 0)
                    return True
                user32.EnumWindows(EnumWindowsProc(cb), 0)
            except Exception:
                pass
            time.sleep(0.5)

    threading.Thread(target=hider, daemon=True).start()

# 别名供 task_debug.py 使用
_start_window_hider = start_window_hider


# ── Chrome driver ──────────────────────────────────────────────────────────

def build_driver(proxy_port: int):
    try:
        import undetected_chromedriver as uc
    except ImportError:
        die("Run: pip install undetected-chromedriver")

    chrome_ver = get_chrome_major_version()
    log(f"Detected Chrome version: {chrome_ver}")

    options = uc.ChromeOptions()

    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-service-autorun")
    options.add_argument("--password-store=basic")
    options.add_argument("--disable-features=ChromeWhatsNewUI")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--window-position=-32000,-32000")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{chrome_ver}.0.0.0 Safari/537.36"
    )
    options.add_argument(f"--proxy-server=http://127.0.0.1:{proxy_port}")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--disable-default-apps")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--blink-settings=imagesEnabled=false")

    stop_prehider = _start_prehider()

    driver = uc.Chrome(
        options=options,
        version_main=chrome_ver,
        suppress_welcome=True,
    )

    stop_prehider()

    if sys.platform == "win32":
        try:
            chrome_pid = driver.browser_pid
            if chrome_pid:
                start_window_hider(chrome_pid)
                log(f"Window hider started for Chrome PID {chrome_pid}")
        except Exception as e:
            log(f"Window hider could not start: {e}", "warn")

    return driver


# ── Scrape ─────────────────────────────────────────────────────────────────

def scrape(driver, url: str, data_queue: queue.Queue) -> list:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    while not data_queue.empty():
        try: data_queue.get_nowait()
        except queue.Empty: break

    driver.get(url)
    driver.execute_script("document.body.style.zoom='50%'")

    btn_locs = [
        (By.XPATH, '//button[.//span[normalize-space(text())="Accept & Continue"]]'),
        (By.XPATH, '//button[@data-bdd="accept-modal-accept-button"]'),
    ]
    try:
        btn = WebDriverWait(driver, 20).until(
            EC.any_of(*[EC.presence_of_element_located(l) for l in btn_locs])
        )
        btn.click()
    except Exception:
        pass

    try:
        WebDriverWait(driver, 25).until(
            EC.visibility_of_any_elements_located((By.XPATH, '//div[@data-analytics="offer-card"]'))
        )
    except Exception:
        log("Offer cards not visible", "warn")

    try:
        zoom = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Zoom In on Interactive Seat Map"]'))
        )
        zoom.click()
    except Exception:
        pass

    time.sleep(8)

    facets_data = offer_data = None
    deadline = time.time() + 5
    while time.time() < deadline:
        while not data_queue.empty():
            try:
                key, data = data_queue.get_nowait()
                if key == "facets": facets_data = data
                else:               offer_data  = data
            except queue.Empty:
                break
        if facets_data and offer_data:
            break
        time.sleep(0.3)

    if not facets_data or not offer_data:
        log(
            f"API capture incomplete "
            f"(facets={'ok' if facets_data else 'missing'}, "
            f"offer={'ok' if offer_data else 'missing'})",
            "warn"
        )
        return []

    try:
        offer_list = offer_data["_embedded"]["offer"]
    except (KeyError, TypeError):
        log("Unexpected offer JSON structure", "warn")
        return []

    price_map = {o["offerId"]: o.get("totalPrice") for o in offer_list if o.get("offerId")}

    place_to_offer = {}
    for facet in facets_data.get("facets", []):
        oids = facet.get("offers", [])
        oid  = oids[0] if isinstance(oids, list) and oids else oids
        for raw in facet.get("places", []):
            for pid in expand_custom(raw):
                place_to_offer[pid] = oid

    from lxml import html as lxhtml
    tree = lxhtml.fromstring(driver.page_source)
    tickets = []

    for block in tree.xpath('//*[local-name()="g" and @data-component="svg__block"]'):
        section = block.get("data-section-name", "")
        for row_el in block.xpath('.//*[local-name()="g" and @data-component="svg__row"]'):
            row = row_el.get("data-row-name", "")
            for seat in row_el.xpath(
                './/*[(local-name()="circle" or local-name()="g") and @data-component="svg__seat"]'
            ):
                cls = seat.get("class", "")
                if   "is-resale"    in cls: branding = "Verified Resale Ticket"
                elif "is-locked"    in cls: branding = "Standard Admission/Unlock"
                elif "is-vip-star"  in cls: branding = "VIP Package"
                elif "is-ada"       in cls: branding = "Standard Admission/Wheelchair Accessible"
                elif "is-available" in cls: branding = "Standard Admission"
                else: continue

                place_id = seat.get("id", "")
                oid      = place_to_offer.get(place_id)
                tickets.append({
                    "description": f"Sec {section} · Row {row} · Seat {seat.get('data-seat-name','?')}",
                    "section":  section,
                    "row":      row,
                    "branding": branding,
                    "price":    price_map.get(oid) if oid else None,
                    "offerId":  oid,
                })
    return tickets


# ── Filter ─────────────────────────────────────────────────────────────────

def apply_filters(tickets, config):
    min_p  = float(config.get("minPrice") or 0)
    max_p  = float(config.get("maxPrice") or 1e9)
    t_type = config.get("tickType", "any")
    out = []
    for t in tickets:
        p = t.get("price")
        if p is not None:
            try:
                if float(p) < min_p or float(p) > max_p: continue
            except (ValueError, TypeError): pass
        if t_type != "any" and t.get("branding") != t_type: continue
        out.append(t)
    return out


# ── Email ──────────────────────────────────────────────────────────────────

def send_email(to, tickets, url):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🎟 TicketWatch: {len(tickets)} ticket(s) found!"
        msg["From"] = SMTP_USER
        msg["To"]   = to

        rows = "".join(
            f"<tr style='border-bottom:1px solid #222'>"
            f"<td style='padding:10px 14px;color:#e8e8f0'>{t.get('description','')}</td>"
            f"<td style='padding:10px 14px;color:#00e5a0;font-family:monospace'>"
            f"{'$'+str(t['price']) if t.get('price') else 'N/A'}</td>"
            f"<td style='padding:10px 14px;color:#aaa'>{t.get('branding','')}</td></tr>"
            for t in tickets[:20]
        )

        body = f"""<html><body style="background:#0a0a0f;color:#e8e8f0;font-family:sans-serif;padding:24px">
  <h2 style="color:#ff3b5c">🎟 TicketWatch Alert</h2>
  <p style="color:#888">Found <strong style="color:#e8e8f0">{len(tickets)}</strong> matching tickets at<br>
    <a href="{url}" style="color:#7c3aed">{url}</a></p>
  <table width="100%" cellspacing="0" style="background:#0e0e1a;border:1px solid #1e1e36;border-radius:8px">
    <thead><tr style="background:#141424">
      <th style="padding:10px 14px;text-align:left;color:#888;font-size:11px">SEAT</th>
      <th style="padding:10px 14px;text-align:left;color:#888;font-size:11px">PRICE</th>
      <th style="padding:10px 14px;text-align:left;color:#888;font-size:11px">TYPE</th>
    </tr></thead><tbody>{rows}</tbody>
  </table>
  <p style="color:#444;font-size:11px;margin-top:24px">Sent by TicketWatch</p>
</body></html>"""

        msg.attach(MIMEText(body, "html"))
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.ehlo(); s.starttls()
            s.login(SMTP_USER, SMTP_PASSWORD)
            s.sendmail(SMTP_USER, to, msg.as_string())

        emit({"type": "email_sent", "to": to})
        log(f"Email sent to {to} ({len(tickets)} tickets)", "success")
    except Exception as e:
        log(f"Email failed: {e}", "error")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0
        )

    if len(sys.argv) < 2:
        die("No config JSON provided")
    try:
        config = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        die(f"Invalid config JSON: {e}")

    url      = config.get("url", "")
    email    = config.get("email", "")
    interval = int(config.get("interval", 300))

    if not url or not email:
        die("url and email are required")

    PROXY_PORT = 18080
    data_queue = queue.Queue()
    addon      = TicketmasterAddon(data_queue)

    threading.Thread(target=run_proxy, args=(PROXY_PORT, addon), daemon=True).start()
    time.sleep(1.5)
    log(f"Proxy listening on port {PROXY_PORT}")

    log("Initializing Chrome…")
    try:
        driver = build_driver(PROXY_PORT)
    except Exception as e:
        die(f"Chrome init failed: {e}\n{traceback.format_exc()}")

    def shutdown(sig, frame):
        log("Shutting down…", "warn")
        try: driver.quit()
        except Exception: pass
        sys.exit(0)

    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    last_seen = set()

    while True:
        try:
            log(f"Checking: {url}")
            tickets = scrape(driver, url, data_queue)
            matched = apply_filters(tickets, config)
            new     = [t for t in matched if t["description"] not in last_seen]

            emit({"type": "check_done", "count": len(new), "total": len(tickets)})
            for t in new:
                emit({"type": "ticket", "ticket": t})
                last_seen.add(t["description"])
            if new:
                send_email(email, new, url)

        except Exception as e:
            log(f"Scrape error: {e}", "error")

        log(f"Next check in {interval}s…")
        time.sleep(interval)


if __name__ == "__main__":
    main()