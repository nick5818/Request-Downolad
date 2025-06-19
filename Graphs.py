import rasterio
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime

# Load all raster paths (assumed sorted)
raster_files = sorted(glob.glob(r'your\path\*.tif'))
raster_files = sorted(glob.glob(r'your\path\*.tif'))
raster_files = sorted(glob.glob(r'your\path\*.tif'))
mean_values = []
dates = []

# Start from Jan 1 and add 10 days per file
start_date = datetime.date(2018, 1, 10)

for i, raster_path in enumerate(raster_files):
    with rasterio.open(raster_path) as src:
        data = src.read(1).astype('float32')
        data[data == src.nodata] = np.nan  # mask NoData
        mean_val = np.nanmean(data)
        mean_values.append(mean_val)
        dates.append(start_date + datetime.timedelta(days=10 * i))


# Choose to plot one of them
plt.figure(figsize=(10, 5))
plt.plot(dates, mean_values, marker='o', linestyle='-', color='green')
plt.title('Fraction of Green Vegetation Cover - 2018')
plt.xlabel('Date')
plt.ylabel('Mean FCover')
plt.grid(True)
plt.tight_layout()
plt.show()


