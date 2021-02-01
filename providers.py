from csv import DictWriter
from datetime import datetime
import json
from operator import itemgetter
from shutil import copyfile
from urllib import request
from zoneinfo import ZoneInfo

LAST_EDITED_ENDPOINT = "https://services5.arcgis.com/Rvw11bGpzJNE7apK/ArcGIS/rest/services/VaccinesPublic_gdb/FeatureServer/1/?f=json"
DATA_ENDPOINT = "https://services5.arcgis.com/Rvw11bGpzJNE7apK/ArcGIS/rest/services/VaccinesPublic_gdb/FeatureServer/1/query?where=1%3D1&outFields=*&maxRecordCountFactor=5&geometryPrecision=6&outSR=%7B%22wkid%22%3A+4326%7D&f=json"

CENTRAL_TZ = ZoneInfo("America/Chicago")
LATEST_PATH = "providers/latest.csv"


def main():
    # hit the metadata endpoint to find the last edit time
    response = request.urlopen(LAST_EDITED_ENDPOINT)
    data = json.load(response)

    # it comes down in like nanoseconds so we need to peel it back a little
    last_edited = datetime.fromtimestamp(
        data["editingInfo"]["lastEditDate"] / 1000.0, tz=CENTRAL_TZ
    )
    as_of = last_edited.date().isoformat()

    # now grab the data itself
    response = request.urlopen(DATA_ENDPOINT)
    data = json.load(response)

    providers = []

    for provider in data["features"]:
        attributes = provider["attributes"]
        geometry = provider.get("geometry", {"x": None, "y": None})

        providers.append({**attributes, **geometry})

    # go a few steps in so we can get what we need out of the Arc data structure
    providers = sorted(providers, key=itemgetter("OBJECTID"))

    # I found a way to trick the FeatureServer into giving me all providers in
    # a single query but this could blow up at any point, so let's check
    assert (
        len(providers) > 1000
    ), "The query returned 1,000 or less providers, something is fishy"

    fieldnames = providers[0].keys()

    with open(LATEST_PATH, "w") as outfile:
        writer = DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerows(providers)

    copyfile(LATEST_PATH, f"providers/snapshots/{as_of}.csv")


if __name__ == "__main__":
    main()