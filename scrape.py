"""
scrape.py (versi Open-Meteo - PM2.5 ASLI, bukan estimasi)
Dijalankan otomatis oleh GitHub Actions (lihat .github/workflows/scrape.yml).
Setiap kali dijalankan, 1 baris data baru ditambahkan ke data_scraping.csv.

Tidak perlu API key -> tidak perlu setup GitHub Secret sama sekali.
"""

import requests
import pandas as pd
import os
from datetime import datetime

LAT, LON = -6.2088, 106.8456  # Jakarta
CSV_PATH = "data_scraping.csv"


def extract():
    aq = requests.get(
        "https://air-quality-api.open-meteo.com/v1/air-quality",
        params={"latitude": LAT, "longitude": LON, "current": "pm2_5"},
        timeout=15,
    ).json()

    wx = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": LAT, "longitude": LON,
                "current": "temperature_2m,wind_speed_10m"},
        timeout=15,
    ).json()

    return aq, wx


def transform(aq, wx):
    return {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
        "pm25": aq["current"]["pm2_5"],                     # <- PM2.5 asli (µg/m³)
        "suhu": wx["current"]["temperature_2m"],
        "kec_angin": wx["current"]["wind_speed_10m"],
    }


def load(record):
    df_new = pd.DataFrame([record])
    if os.path.exists(CSV_PATH):
        df_new.to_csv(CSV_PATH, mode="a", header=False, index=False)
    else:
        df_new.to_csv(CSV_PATH, mode="w", header=True, index=False)


if __name__ == "__main__":
    aq, wx = extract()
    record = transform(aq, wx)
    load(record)
    print(f"Data ditambahkan: {record}")
