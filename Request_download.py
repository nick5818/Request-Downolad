import os
from hda import Client, Configuration

# Specify the path to the config file
# Must log in to https://wekeo.copernicus.eu

config = Configuration(user = "", password = "")
hda_client = Client(config = config)
print(hda_client)

# Set multiple AOIs 
aoi_bbox = [

{
  "lonmin": 17.75,
  "latmin": 59.22,
  "lonmax": 18.2,
  "latmax": 59.43
},

{
  "lonmin": 9.74,
  "latmin": 54.88,
  "lonmax": 9.84,
  "latmax": 54.94
},

{
  "lonmin": 8.42,
  "latmin": 49.44,
  "lonmax": 8.52,
  "latmax": 49.54
}
]

# Set multiple API requests.
# In this case FCOVER, LAI and FAPAR.
# Visit https://wekeo.copernicus.eu/data?view=catalogue to get other API requests.

apis = [
# FCOVER
{
  "dataset_id": "EO:CLMS:DAT:CLMS_GLOBAL_FCOVER_300M_V1_10DAILY_NETCDF",
  "productType": "FCOVER300",
  "productionStatus": "ARCHIVED",
  "acquisitionType": "NOMINAL",
  "platform": "PROBA-V",
  "processingCenter": "VITO",
  "productGroupId": "RT2",
  "start": "2018-03-31T00:00:00.000Z",
  "end": "2018-03-31T23:59:59.999Z",
  "itemsPerPage": 200,
  "startIndex": 0
},

# LAI
{
  "dataset_id": "EO:CLMS:DAT:CLMS_GLOBAL_LAI_300M_V1_10DAILY_NETCDF",
  "productType": "LAI300",
  "productionStatus": "ARCHIVED",
  "acquisitionType": "NOMINAL",
  "platform": "PROBA-V",
  "processingCenter": "VITO",
  "productGroupId": "RT2",
  "resolution": "300",
  "start": "2018-07-20T00:00:00.000Z",
  "end": "2018-07-20T23:59:59.999Z",
  "itemsPerPage": 200,
  "startIndex": 0
},

# FAPAR
{
  "dataset_id": "EO:CLMS:DAT:CLMS_GLOBAL_FAPAR_300M_V1_10DAILY_NETCDF",
  "productType": "FAPAR300",
  "productionStatus": "ARCHIVED",
  "acquisitionType": "NOMINAL",
  "platform": "PROBA-V",
  "processingCenter": "VITO",
  "productGroupId": "RT2",
  "resolution": "300",
  "start": "2018-01-01T00:00:00.000Z",
  "end": "2018-01-01T23:59:59.999Z",
  "itemsPerPage": 200,
  "startIndex": 0
}
]


#### Download Data ####
for api in apis:
    for aoi in aoi_bbox:
        query = api.copy()
        query["bbox"] = [aoi["lonmin"], aoi["latmin"], aoi["lonmax"], aoi["latmax"]]
        mat = hda_client.search(query)
        print(query["productType"], "Vitoria:", mat)
        if query["productType"] == "FCOVER300":
            mat.download(download_dir = r"download dir\fcover")
        elif query["productType"] == "LAI300":
            mat.download(download_dir = r"download dir\lai")
        else:
            mat.download(download_dir = r"download dir\fapar")