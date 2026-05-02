import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

LOGIN_URL = "https://kolvw.caspr.be/login"
AGENDA_URL = "https://kolvw.caspr.be/leerlingapp/Agenda"

USERNAME = os.getenv("CASPR_USERNAME")
PASSWORD = os.getenv("CASPR_PASSWORD")

def agenda_van_morgen():
    morgen = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")

    session = requests.Session()

    # 🔐 Login (kan aangepast moeten worden)
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }

    session.post(LOGIN_URL, data=login_data)
    response = session.get(AGENDA_URL)

    soup = BeautifulSoup(response.text, "html.parser")
    items_morgen = []

    # ⚠️ PAS DIT AAN NA INSPECTEREN
    for item in soup.select(".agenda-item"):
        tekst = item.get_text(" ", strip=True)

        if morgen in tekst:
            items_morgen.append(tekst)

    return items_morgen