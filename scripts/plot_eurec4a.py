import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
# import seaborn as sb
from tqdm import tqdm
import xarray as xr
from gogoesgone import processing as pr
from gogoesgone import zarr_access as za

year = 2020
month = 1
channel = 13
product = "ABI-L2-CMIPF"  #'ABI-L1b-RadF'
satellite = "goes16"  

output_dir = '/Users/acmsavazzi/Documents/WORK/PhD_Year3/DATA/gogoesgone/output/'
# time = "20200101 12:00:00"
def main():
    all_subsets = []  # List to store each subset
    for dayofyear in tqdm(range(1, 15), desc="Processing days"):
        for hour in tqdm(range(1, 24), desc="Processing hours", leave=False):
            time = str(year)+str(month).zfill(2)+str(dayofyear).zfill(2)+' '+str(hour).zfill(2)+':00:00'
            flist = za.nearest_time_url(time)
            m = za.get_mapper_from_mzz(flist)
            img = pr.Image(m)
            extent = (-59, -56, 12, 14)
            subset = img.subset_region_from_latlon_extents(extent, unit="degree")
            all_subsets.append(subset)

    # Concatenate along the 't' dimension and save to a single .nc file
    concatenated = xr.concat(all_subsets, dim='t')
    concatenated.rename({'t':'time'})
    concatenated['CMI'].to_netcdf(output_dir + f'/goes_{year}{str(month).zfill(2)}.nc')

if __name__ == "__main__":
    main()
