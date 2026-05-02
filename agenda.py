from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import os
import time

CASPR_URL = "https://kolvw.caspr.be/leerlingapp/Agenda"

def agenda_van_morgen():
    morgen = (datetime.now() + timedelta(days=1)).strftime("%-d-%-m")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(CASPR_URL)

    # ⏳ Wacht tot agenda‑blokken zichtbaar zijn
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fc-event"))
    )

    time.sleep(2)  # extra buffer

    items_morgen = []

    events = driver.find_elements(By.CLASS_NAME, "fc-event")
    for event in events:
        tekst = event.text.strip()
        if tekst:
            items_morgen.append(tekst)

    driver.quit()
    return items_morgen
