from csv import DictWriter
from datetime import datetime
import json
from operator import itemgetter
from shutil import copyfile
from urllib import request

LAST_EDITED_ENDPOINT = "https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/VaccineProviderLocations/FeatureServer/0/?f=json"
DATA_ENDPOINT = "https://services5.arcgis.com/ACaLB9ifngzawspq/ArcGIS/rest/services/VaccineProviderLocations/FeatureServer/0/query?where=1%3D1&outFields=*&maxRecordCountFactor=5&f=json"

LATEST_PATH = "providers/latest.csv"


def main():
    # hit the metadata endpoint to find the last edit time
    response = request.urlopen(LAST_EDITED_ENDPOINT)
    data = json.load(response)

    # it comes down in like nanoseconds so we need to peel it back a little
    last_edited = datetime.fromtimestamp(data["editingInfo"]["lastEditDate"] / 1000.0)
    as_of = last_edited.date().isoformat()

    # now grab the data itself
    response = request.urlopen(DATA_ENDPOINT)
    data = json.load(response)

    # go a few steps in so we can get what we need out of the Arc data structure
    providers = sorted(
        (d["attributes"] for d in data["features"]), key=itemgetter("OBJECTID")
    )

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