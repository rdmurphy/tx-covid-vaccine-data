#!/bin/bash

# the raw output JSON
FILE=latest.json

LAST_EDITED=$(curl "https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/VaccineProviderLocations/FeatureServer/0/?f=json" | jq ".editingInfo.lastEditDate")
RAW_JSON=$(curl "https://services5.arcgis.com/ACaLB9ifngzawspq/ArcGIS/rest/services/VaccineProviderLocations/FeatureServer/0/query?where=1%3D1&outFields=*&maxRecordCountFactor=5&f=pjson" | jq "[.features | .[] | .attributes] | sort_by(.OBJECTID)")

echo -n "$RAW_JSON" > "snapshots/$LAST_EDITED.json"
echo -n "$RAW_JSON" > "$FILE"
