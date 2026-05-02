from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time

CASPR_URL = "https://kolvw.caspr.be/leerlingapp/Agenda"

def agenda_van_morgen():
    morgen = (datetime.now() + timedelta(days=1)).strftime("%d-%m")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(CASPR_URL)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fc-event"))
    )

    time.sleep(1)

    items = []
    events = driver.find_elements(By.CLASS_NAME, "fc-event")

    for e in events:
        tekst = e.text.strip()
        if tekst:
            items.append(tekst)

    driver.quit()
    return items
