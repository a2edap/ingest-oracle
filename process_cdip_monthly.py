import os
import numpy as np
import xarray as xr
from glob import glob
from pathlib import Path


# Fetch all the cdip files
filelist = glob("/share/data/cdip/*/*.nc")

for file in filelist:
    ds = xr.open_dataset(file)
    print(file)

    # Fix other dataset problems
    if ds.dataset_name in ["067", "142", "153"]:
        ds["time"] = xr.DataArray(ds["time"].values, dims=["time"])
        ds["sst_time"] = xr.DataArray(ds["sst_time"].values, dims=["sst_time"])
        ds["gps_time"] = xr.DataArray(ds["gps_time"].values, dims=["gps_time"])
        wave_vars = [w for w in ds.data_vars if "wave" in w]
        for var in wave_vars:
            ds[var] = (
                ds[var]
                .assign_coords(dwr_time=ds["time"].values)
                .rename(dwr_time="time")
            )

    # Get the start and end month
    t0 = ds.time[0].values
    t1 = ds.time[-1].values
    list_of_dates = np.arange(t0, t1, dtype="M8[M]")
    # Hack last month on to end
    try:
        list_of_dates = np.append(
            list_of_dates, list_of_dates[-1] + np.timedelta64(1, "M")
        )
    except:  # brand new files
        list_of_dates = [t0.astype("M8[M]")]

    # Save each month as an individual file
    for date in list_of_dates:
        time_slc = slice(date, date + np.timedelta64(1, "M"))
        time_coords = [t for t in ds.coords if "time" in t]
        time_dict = dict.fromkeys(time_coords, time_slc)

        try:
            ds_slice = ds.loc[time_dict]
        except:
            # Fix persistantly mixed up time coordinates
            for tc in time_coords:
                ds = ds.sortby(tc)
            ds_slice = ds.loc[time_dict]

        try:
            ds_slice.attrs["time_coverage_start"] = str(
                ds_slice[time_coords[0]][0].values
            )
            ds_slice.attrs["time_coverage_end"] = str(
                ds_slice[time_coords[0]][-1].values
            )
        except:
            pass

        # Create new filepath with start year/month
        datastream = ".".join(Path(file).stem.split(".")[:3])
        new_filepath = Path(f"/share/data/cdip_monthly/{datastream}")
        new_filename = datastream + "." + str(date).replace("-", "") + ".nc"

        if not os.path.exists(new_filepath):
            os.makedirs(new_filepath)

        if ds_slice.time.size:  # For files with missing timestamps
            ds_slice.to_netcdf(new_filepath / new_filename)
