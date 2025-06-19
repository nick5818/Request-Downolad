import os
import glob
import xarray as xr
import geopandas as gpd
import rioxarray
from rasterio.enums import Resampling

# Set main path
ff_nc = "\your_path (nc files)"

# Create folders in your path
nc_folder    = os.path.join(ff_nc, "nc") # NetCDF files
gpkg_folder  = os.path.join(ff_nc, "Shps") # Geopackage or shapefile of aoi
output_base  = os.path.join(ff_nc, "Outputs") # Clipped files
target_var   = "variable you want (FCOVER/LAI etc.)"
city_name    = "Name of the aoi you want to clip" # Will create an extra folder with the name of the aoi
layer_name   = "not needed if you do not have a gkpg" # If you do, add the exact name of the layer, better load it on QGIS to see

# load aoi boundary 
gpkgs = glob.glob(os.path.join(gpkg_folder, f"*{city_name}*.gpkg"))
gdf = gpd.read_file(gpkgs[0], layer=layer_name).to_crs("EPSG:4326") # gpkgs[0] in case you have more files in the folder (select the first one)

def clip():
    for nc_path in glob.glob(os.path.join(nc_folder, "*.nc")):
        fn = os.path.basename(nc_path)
        print(f"[FCOVER] → {fn}")
        try:
            ds = xr.open_dataset(nc_path, decode_timedelta=False)
            da = ds[target_var]
            da.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
            da.rio.write_crs("EPSG:4326", inplace=True)
            da_clip = da.rio.clip(gdf.geometry.values, gdf.crs, drop=True)
        except Exception as e:
            print(f"  SKIP {fn}: {e}")
            continue

        out_dir = os.path.join(output_base, city_name)
        os.makedirs(out_dir, exist_ok=True)
        out_nc = os.path.join(out_dir, fn.replace(".nc", f"_{target_var}_clipped.nc"))
        try:
            da_clip.to_netcdf(out_nc)
            print(f"  DONE {out_nc}")
        except Exception as e:
            print(f"  SKIP write failed: Possibly corrupted .nc file. Re-download {e}")

clip()

def to_rast():
    clipped_folder = os.path.join(output_base, city_name)
    output_tiff_folder = os.path.join(clipped_folder, "Geotiffs") # Creates a folder in the folder with the clipped files
    os.makedirs(output_tiff_folder, exist_ok=True)

    for nc_file in glob.glob(os.path.join(clipped_folder, f"*_{target_var}_clipped.nc")):
        base = os.path.basename(nc_file)
        tif  = base.replace(".nc", ".tif")
        out  = os.path.join(output_tiff_folder, tif)
        print(f"[Convert] → {base}")
        try:
            ds = xr.open_dataset(nc_file)
            da = ds[target_var]
            if not da.rio.crs:
                da = da.rio.write_crs("EPSG:4326")
            da.rio.to_raster(out)
            print(f"  DONE {out}")
        except Exception as e:
            print(f"  SKIP: Possibly corrupted .nc file. Re-download {base}: {e}")

to_rast()