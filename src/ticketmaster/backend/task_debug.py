#!/usr/bin/env python3

import sys
import json
import time
import gzip
import traceback
import threading
import queue
from io import BytesIO

TEST_URL     = "https://www.ticketmaster.ca/twice-this-is-for-world-tour-hamilton-ontario-03-07-2026/event/1000633AAE9457A3"
PROXY_PORT   = 18080
WAIT_SECONDS = 12

try:
    import colorama; colorama.init()
    G="\033[92m"; Y="\033[93m"; R="\033[91m"; C="\033[96m"; B="\033[1m"; E="\033[0m"
except ImportError:
    G=Y=R=C=B=E=""

def ok(m):   print(f"{G}  ✓  {E}{m}")
def warn(m): print(f"{Y}  ⚠  {E}{m}")
def err(m):  print(f"{R}  ✗  {E}{m}")
def info(m): print(f"{C}  ·  {E}{m}")
def sep(t):  print(f"\n{B}{'═'*55}\n  {t}\n{'═'*55}{E}")


class DebugAddon:
    def __init__(self, q):
        self.q = q
        self.all_urls = []

    def response(self, flow):
        url = flow.request.url

        if "ticketmaster" in url.lower():
            self.all_urls.append(url)

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

        label = "FACETS" if is_facets else "OFFER"
        print(f"{G}  [PROXY CAPTURED] {label}{E} → {url[:90]}…")

        try:
            body = flow.response.content
            if not body:
                print(f"{Y}  [PROXY] empty body, skipping{E}")
                return

            enc = flow.response.headers.get("content-encoding", "")
            if "gzip" in enc:
                try:
                    with gzip.GzipFile(fileobj=BytesIO(body)) as f:
                        body = f.read()
                except Exception:
                    pass

            text = body.decode("utf-8").strip()
            if not text:
                return

            data = json.loads(text)
            key  = "facets" if is_facets else "offer"
            print(f"{G}  [PROXY DECODED] {key} — {len(str(data))} chars{E}")
            self.q.put((key, data))
        except Exception as e:
            print(f"{R}  [PROXY DECODE ERROR] {e} | body[:80]={flow.response.content[:80]}{E}")

from task import (
    build_driver,
    # start_window_hider,
    get_chrome_major_version,
    run_proxy,
    expand_custom,
)

def main():
    sep("STEP 1 — Start mitmproxy")
    data_queue = queue.Queue()
    addon      = DebugAddon(data_queue)
    t = threading.Thread(target=run_proxy, args=(PROXY_PORT, addon), daemon=True)
    t.start()
    time.sleep(1.5)
    ok(f"Proxy listening on 127.0.0.1:{PROXY_PORT}")

    sep("STEP 2 — Launch Chrome")
    try:
        driver = build_driver(PROXY_PORT)
        ok("Chrome started")
    except Exception as e:
        err(f"Chrome failed: {e}")
        traceback.print_exc()
        sys.exit(1)

    sep("STEP 3 — Load page")
    info(f"URL: {TEST_URL}")
    try:
        driver.get(TEST_URL)
        driver.execute_script("document.body.style.zoom='50%'")
        ok("Page loaded")
    except Exception as e:
        err(f"Page load failed: {e}")

    sep("STEP 4 — Handle cookie modal")
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    btn_locs = [
        (By.XPATH, '//button[.//span[normalize-space(text())="Accept & Continue"]]'),
        (By.XPATH, '//button[@data-bdd="accept-modal-accept-button"]'),
    ]
    try:
        btn = WebDriverWait(driver, 20).until(
            EC.any_of(*[EC.presence_of_element_located(l) for l in btn_locs])
        )
        btn.click()
        ok("Modal accepted")
    except Exception:
        warn("No modal found (already accepted or not shown)")

    sep("STEP 5 — Wait for offer cards")
    try:
        WebDriverWait(driver, 25).until(
            EC.visibility_of_any_elements_located((By.XPATH, '//div[@data-analytics="offer-card"]'))
        )
        ok("Offer cards visible")
    except Exception:
        warn("Offer cards not found — page may have changed layout")

    sep("STEP 6 — Click zoom on seat map")
    try:
        zoom = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Zoom In on Interactive Seat Map"]'))
        )
        zoom.click()
        ok("Zoom clicked")
    except Exception:
        warn("Zoom button not found")

    sep(f"STEP 7 — Waiting {WAIT_SECONDS}s for API calls…")
    for i in range(WAIT_SECONDS, 0, -1):
        print(f"\r  {C}waiting {i}s…{E}   ", end="", flush=True)
        time.sleep(1)
    print()

    sep("STEP 8 — Collect proxy data")
    facets_data = offer_data = None
    deadline = time.time() + 5
    while time.time() < deadline:
        while not data_queue.empty():
            try:
                key, data = data_queue.get_nowait()
                if key == "facets":
                    facets_data = data
                    ok(f"facets.json captured — {len(data.get('facets', []))} facets")
                else:
                    offer_data = data
                    n = len(data.get("_embedded", {}).get("offer", []))
                    ok(f"offer.json captured — {n} offers")
            except queue.Empty:
                break
        if facets_data and offer_data:
            break
        time.sleep(0.2)

    if not facets_data:
        err("facets data MISSING")
    if not offer_data:
        err("offer data MISSING")

    if addon.all_urls:
        print(f"\n{Y}  All Ticketmaster URLs captured by proxy ({len(addon.all_urls)} total):{E}")
        for u in addon.all_urls[-20:]:
            print(f"    {u[:110]}")
    else:
        err("No Ticketmaster URLs captured at all — proxy may not be routing traffic")
        print(f"\n{Y}  Possible causes:{E}")
        print("    1. Chrome is not using the proxy (check --proxy-server arg)")
        print("    2. mitmproxy cert not trusted (try running once manually first)")
        print("    3. URL patterns changed — check URLs above vs addon filter")

    if not facets_data or not offer_data:
        print(f"\n{R}  Cannot continue without both data sources. Saving page source…{E}")
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        ok("Saved debug_page.html — open it and check if the seat map loaded")
        driver.quit()
        sys.exit(1)

    sep("STEP 9 — Parse tickets")
    offers    = offer_data["_embedded"]["offer"]
    price_map = {o["offerId"]: o.get("totalPrice") for o in offers if o.get("offerId")}
    info(f"Price map: {len(price_map)} entries")

    place_to_offer = {}
    for facet in facets_data.get("facets", []):
        oids = facet.get("offers", [])
        oid  = oids[0] if isinstance(oids, list) and oids else oids
        for raw in facet.get("places", []):
            for pid in expand_custom(raw):
                place_to_offer[pid] = oid
    info(f"Place map: {len(place_to_offer)} seat IDs")

    from lxml import html as lxhtml
    tree    = lxhtml.fromstring(driver.page_source)
    tickets = []
    blocks  = tree.xpath('//*[local-name()="g" and @data-component="svg__block"]')
    info(f"SVG blocks found: {len(blocks)}")

    for block in blocks:
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
                price    = price_map.get(oid) if oid else None
                tickets.append({
                    "description": f"Sec {section} · Row {row} · Seat {seat.get('data-seat-name','?')}",
                    "section":  section,
                    "row":      row,
                    "branding": branding,
                    "price":    price,
                    "offerId":  oid,
                })

    sep("STEP 10 — Results")
    if not tickets:
        warn("No tickets parsed from SVG")
        print(f"\n{Y}  Possible causes:{E}")
        print("    1. Seat map not fully loaded — try increasing WAIT_SECONDS (currently", WAIT_SECONDS, ")")
        print("    2. SVG structure changed — check debug_page.html")
        print("    3. Event sold out / no available seats")
    else:
        ok(f"Found {len(tickets)} total seats")

        from collections import Counter
        counts = Counter(t["branding"] for t in tickets)
        for brand, n in counts.most_common():
            info(f"  {brand}: {n}")

        print(f"\n{B}  Sample tickets (first 10):{E}")
        for t in tickets[:10]:
            price_str = f"${t['price']}" if t.get("price") else "N/A"
            print(f"    {G}{price_str:>10}{E}  {t['description'][:55]}  [{t['branding']}]")

        with open("debug_result.json", "w", encoding="utf-8") as f:
            json.dump(tickets, f, indent=2, ensure_ascii=False)
        ok(f"Full results saved to debug_result.json ({len(tickets)} tickets)")

    driver.quit()
    ok("Chrome closed. Done.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("\n[ERROR] Press Enter to exit...")