"""
one-off script used to acquire the data (not needed to do the assignment)

earthquakes in California, from the USGS catalog
https://earthquake.usgs.gov/fdsnws/event/1/
"""
import io
import requests
import pandas as pd

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

r = requests.get(
    URL,
    params={
        "format": "csv",
        "starttime": "2025-10-01",
        "endtime": "2026-10-01",
        "minmagnitude": 2.5,
        "minlatitude": 32,
        "maxlatitude": 42,
        "minlongitude": -125,
        "maxlongitude": -114,
        "orderby": "time-asc",
    },
)
r.raise_for_status()
df = pd.read_csv(io.StringIO(r.text))
df = df[["time", "latitude", "longitude", "depth", "mag", "place", "type"]]
df.to_csv("data/quakes.csv", index=False)
print("quakes", df.shape)
print(df.type.value_counts())
