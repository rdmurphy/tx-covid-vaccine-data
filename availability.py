from csv import DictWriter
import json
from operator import itemgetter
from shutil import copyfile
from urllib import request

LAST_EDITED_ENDPOINT = "https://services1.arcgis.com/Z3qsB1OAIjFLs23T/ArcGIS/rest/services/Vaccines/FeatureServer/0/?f=json"
DATA_ENDPOINT = "https://services1.arcgis.com/Z3qsB1OAIjFLs23T/ArcGIS/rest/services/Vaccines/FeatureServer/0/query?where=1%3D1&outFields=*&maxRecordCountFactor=5&f=json"

LATEST_PATH = "availability/latest.csv"


def main():
    # hit the metadata endpoint to find the last edit time
    response = request.urlopen(LAST_EDITED_ENDPOINT)
    data = json.load(response)

    if "error" in data:
        return

    # use the raw timestamp in case this changes more frequently
    as_of = data["editingInfo"]["lastEditDate"]

    # now grab the data itself
    response = request.urlopen(DATA_ENDPOINT)
    data = json.load(response)

    # go a few steps in so we can get what we need out of the Arc data structure
    providers = sorted(
        (d["attributes"] for d in data["features"]), key=itemgetter("ObjectId")
    )

    fieldnames = providers[0].keys()

    with open(LATEST_PATH, "w") as outfile:
        writer = DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerows(providers)

    copyfile(LATEST_PATH, f"availability/snapshots/{as_of}.csv")


if __name__ == "__main__":
    main()