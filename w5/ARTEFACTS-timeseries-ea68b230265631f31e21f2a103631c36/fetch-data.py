"""
one-off script used to acquire the data (not needed by students)

* bike counter: Paris open data, https://opendata.paris.fr
  dataset comptage-velo-donnees-compteurs, a single counter, hourly
* weather: Open-Meteo archive API, https://open-meteo.com, Paris, daily
"""
import requests
import pandas as pd

COUNTER = "Voie Georges Pompidou NE-SO"

# --- bike counter
URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-donnees-compteurs/exports/json"
r = requests.get(
    URL,
    params={
        "select": "date,sum_counts",
        "where": f'nom_compteur="{COUNTER}"',
        "order_by": "date",
    },
)
r.raise_for_status()
df = pd.DataFrame(r.json())
df["date"] = pd.to_datetime(df["date"], utc=True)
# like the original export: local time, with the UTC offset - which changes with DST
df["date"] = df["date"].dt.tz_convert("Europe/Paris").map(lambda t: t.isoformat())
df = df.rename(columns={"date": "timestamp", "sum_counts": "count"})
df.to_csv("data/bike-counter.csv", index=False)
print("bike-counter", df.shape, df.timestamp.iloc[0], df.timestamp.iloc[-1])

# --- weather
r = requests.get(
    "https://archive-api.open-meteo.com/v1/archive",
    params={
        "latitude": 48.85,
        "longitude": 2.35,
        "start_date": "2025-09-12",
        "end_date": "2026-10-11",
        "daily": "temperature_2m_mean,precipitation_sum",
        "timezone": "Europe/Paris",
    },
)
r.raise_for_status()
daily = r.json()["daily"]
weather = pd.DataFrame(
    {
        # on purpose: french format, so that students have to say what they mean
        "jour": pd.to_datetime(daily["time"]).strftime("%d/%m/%Y"),
        "temperature": daily["temperature_2m_mean"],
        "rain_mm": daily["precipitation_sum"],
    }
)
weather.to_csv("data/weather.csv", index=False)
print("weather", weather.shape)
