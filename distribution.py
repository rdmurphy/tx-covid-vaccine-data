import csv
from io import BytesIO
from shutil import copyfile
from urllib import request
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

PATH_TO_EXCEL = (
    "https://www.dshs.texas.gov/immunize/covid19/COVID-19-Vaccine-Data-by-County.xls"
)
CENTRAL_TZ = ZoneInfo("America/Chicago")
LATEST_PATH = "distribution/latest.csv"


def main():
    # load the file and convert it into a file-object
    response = request.urlopen(PATH_TO_EXCEL)
    file = BytesIO(response.read())

    # pass into openpyxl and find when it was last modified
    wb = load_workbook(file, read_only=True, data_only=True)
    # we convert it to Central time because Texas (sorry, El Paso)
    modified = wb.properties.modified.astimezone(tz=CENTRAL_TZ)
    # now we have a timezone aware ISO date
    as_of = modified.date().isoformat()

    # grab our "Data" sheet
    sheet = wb["By County"]

    # save out our latest fil
    with open(LATEST_PATH, "w") as outfile:
        writer = csv.writer(outfile)

        for row in sheet.rows:
            writer.writerow(cell.value for cell in row)

    # don't need the notebook anymore
    wb.close()

    copyfile(LATEST_PATH, f"distribution/snapshots/{as_of}.csv")


if __name__ == "__main__":
    main()