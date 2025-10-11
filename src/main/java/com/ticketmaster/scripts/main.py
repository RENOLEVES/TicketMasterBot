from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
import time
import gzip
import json


def fetch_data(url):
    options = ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--disable-extensions')

    driver = Chrome(options=options)

    driver.get(url)

    driver.execute_script("document.body.style.zoom='50%'")

    button_locators = [
        (By.XPATH, '//button[.//span[normalize-space(text())="Accept & Continue"]]'),
        (By.XPATH, '//button[@data-bdd="accept-modal-accept-button"]')
    ]

    wait = WebDriverWait(driver, 20)
    button = wait.until(
        EC.any_of(
            *[EC.presence_of_element_located(locator) for locator in button_locators]
        )
    )
    button.click()

    offer_card_locator = (By.XPATH, '//div[@data-analytics="offer-card"]')
    WebDriverWait(driver, 25).until(EC.visibility_of_any_elements_located(offer_card_locator))

    time.sleep(1)

    # zoom in the map
    zoom_btn_locator = (By.XPATH, '//button[@aria-label="Zoom In on Interactive Seat Map"]')
    zoom_btn = WebDriverWait(driver, 25).until(EC.element_to_be_clickable(zoom_btn_locator))
    if zoom_btn:
        zoom_btn.click()

    time.sleep(10)

    for request in driver.requests:
        if request.response:

            if "services.ticketmaster.ca/api/ismds/event" in request.url and "facets?by=section+seating" in request.url:
                print("capture facets request URL：", request.url)
                if "gzip" in request.response.headers.get('Content-Encoding', ''):

                    compressed_data = request.response.body
                    with gzip.GzipFile(fileobj=BytesIO(compressed_data), mode='rb') as f:
                        data = f.read()
                        response_data = data.decode('utf-8')
                        json_data = json.loads(response_data)

                        with open("./facets.json", "w", encoding="utf-8") as f:
                            json.dump(json_data, f, indent=2)
                        print("successfully saved facets data：facets.json")
                else:
                    print("convert error")

            if "offeradapter.ticketmaster.ca/api/ismds/event" in request.url and "facets?apikey=" in request.url:
                print("capture facets request URL：", request.url)
                if "gzip" in request.response.headers.get('Content-Encoding', ''):

                    compressed_data = request.response.body
                    with gzip.GzipFile(fileobj=BytesIO(compressed_data), mode='rb') as f:
                        data = f.read()
                        response_data = data.decode('utf-8')
                        json_data = json.loads(response_data)

                        with open("./offer.json", "w", encoding="utf-8") as f:
                            json.dump(json_data, f, indent=2)
                        print("successfully saved facets data：offer.json")
                else:
                    print("convert error")

            if "services.ticketmaster.ca/api/ismds/event" in request.url and "facets?apikey=" in request.url:
                print("capture facets request URL：", request.url)
                if "gzip" in request.response.headers.get('Content-Encoding', ''):

                    compressed_data = request.response.body
                    with gzip.GzipFile(fileobj=BytesIO(compressed_data), mode='rb') as f:
                        data = f.read()
                        response_data = data.decode('utf-8')
                        json_data = json.loads(response_data)

                        with open("./offer.json", "w", encoding="utf-8") as f:
                            json.dump(json_data, f, indent=2)
                        print("successfully saved facets data：offer.json")
                else:
                    print("convert error")


    html = driver.page_source
    file_path = r"./data1.html"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("data written")

    driver.quit()
