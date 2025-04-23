from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
import time
import gzip
import json

options = ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')  # 使用隐身模式
options.add_argument('--disable-extensions')  # 禁用扩展程序

driver = Chrome(options=options)

# url = "https://www.ticketmaster.ca/kip-moore-solitary-tracks-tour-toronto-ontario-04-24-2025/event/1000623BC2FF1C57"

# url = "https://www.ticketmaster.ca/2025-bibi-1st-world-tour-eve-toronto-ontario-06-05-2025/event/10006265B9D820B1"

#black pink
url = "https://www.ticketmaster.ca/blackpink-2025-world-tour-toronto-ontario-07-22-2025/event/10006252DC87273D"
driver.get(url)

time.sleep(10) # Give it time to bypass the verification page

driver.execute_script("document.body.style.zoom='50%'")

# accept cookies
locator = (By.XPATH, '//button[.//span[normalize-space(text())="Accept & Continue"]]')
button = WebDriverWait(driver,20).until(EC.element_to_be_clickable(locator))
if button:
    button.click()

time.sleep(1)

# zoom in the map
zoom_btn_locator = (By.XPATH,'//button[@aria-label="Zoom In on Interactive Seat Map"]')
zoom_btn = WebDriverWait(driver,20).until(EC.element_to_be_clickable(zoom_btn_locator))
if zoom_btn:
    zoom_btn.click()

time.sleep(2)
count = 0
count1 = 0

# 捕获所有请求
for request in driver.requests:
    if request.response:
        # 检查是否是目标请求 URL
        if "services.ticketmaster.ca/api/ismds/event" in request.url and "facets?by=section+seating" in request.url:
            print("✅ capture facets request URL：", request.url)
            if "gzip" in request.response.headers.get('Content-Encoding', ''):
                # 解压 GZIP 响应
                compressed_data = request.response.body
                with gzip.GzipFile(fileobj=BytesIO(compressed_data), mode='rb') as f:
                    data = f.read()
                    response_data = data.decode('utf-8')  # 解码为 UTF-8 字符串
                    json_data = json.loads(response_data)  # 转换为 JSON

                    # 保存数据
                    with open("facets.json", "w", encoding="utf-8") as f:
                        json.dump(json_data, f, indent=2)
                    print("✅ successfully saved facets data：facets.json")
            else:
                print("⚠️ convert error")

        if "offeradapter.ticketmaster.ca/api/ismds/event" in request.url and "facets?apikey=" in request.url:
            print("✅ capture facets request URL：", request.url)
            if "gzip" in request.response.headers.get('Content-Encoding', ''):
                # 解压 GZIP 响应
                compressed_data = request.response.body
                with gzip.GzipFile(fileobj=BytesIO(compressed_data), mode='rb') as f:
                    data = f.read()
                    response_data = data.decode('utf-8')  # 解码为 UTF-8 字符串
                    json_data = json.loads(response_data)  # 转换为 JSON

                    # 保存数据
                    with open("offer.json", "w", encoding="utf-8") as f:
                        json.dump(json_data, f, indent=2)
                    print("✅ successfully saved facets data：offer.json")
            else:
                print("⚠️ convert error")


html = driver.page_source
file_path = r"./data1.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)

print("data written")

# normal exit
time.sleep(2)
driver.quit()
