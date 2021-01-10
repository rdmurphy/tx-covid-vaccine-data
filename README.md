# Texas COVID Vaccine Data

Tracking data on the progress of vaccine distribution and adminstration in Texas.

In addition to surfacing the latest available data the state is providing, this repo is also saving snapshots of each change in each directory's respective `snapshots` folder, enabling over-time analysis (with a little bit of work).

Be aware that the state **has** re-worked a few of the data sets since they created them, so there's no guarantee that every snapshot is compatible with each other.

If there are any other datasets you think are worth including here, please let me know in an issue!

## What's available

### Vaccine Distribution and Allocation by County ([Latest data](distribution/latest.csv))

Initially added to the repo on Dec. 29, 2020.

A backup of the XLSX file made available [on this page](https://www.dshs.texas.gov/immunize/covid19/COVID-19-Vaccine-Data-by-County.xls) on the Texas Department of State Health Services (DSHS) website. This is the same data that is surfaced on the more user-friendly [Tableau dashboard](https://tabexternal.dshs.texas.gov/t/THD/views/COVID-19VaccineinTexasDashboard/Summary).


### Vaccine Allocation by Age and Gender ([Latest data](ages/latest.csv))

Initially added to the repo on Jan. 8, 2021.

This is sourced from the same XLSX file as the data above when it was added as a new sheet on Jan. 8, 2021.

### Vaccine Providers ([Latest data](providers/latest.csv))

Initially added to the repo on Dec. 28, 2020.

This is the data powering Texas' [COVID vaccine provider map](https://tdem.maps.arcgis.com/apps/webappviewer/index.html?id=3700a84845c5470cb0dc3ddace5c376b). It initially tracked how many vaccines had been distrbuted by week, but has since moved to just showing the totals of Pfizer and Moderna vaccines received per location.

### Vaccine Distribution and Availability by Provider ([Latest data](availability/latest.csv))

Initially added to the repo on Dec. 30, 2020.

This is the most detailed data I have found so far. Was initially powering a separate Texas Department of Emergency Management (TDEM) map, but now is the source of whether vaccines are marked as available in the map above.

## License

MIT
