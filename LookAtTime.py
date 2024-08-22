import netCDF4 as nc
from netCDF4 import num2date

# Load the NetCDF file
file_path = "storage/root/data/smode/smode.saildrone_v1.z09.a1/smode.saildrone_v1.z09.a1.20221006.071928.nc"  # Replace with your file path
dataset = nc.Dataset(file_path)

# Check the variables
print("Variables in the dataset:", dataset.variables.keys())

# Extract the time variable
time_var = dataset.variables["time"][:]
time_units = dataset.variables["time"].units  # Get the time units
time_calendar = (
    dataset.variables["time"].calendar
    if "calendar" in dataset.variables["time"].ncattrs()
    else "standard"
)

# Convert numeric time values to datetime objects
time_dates = num2date(time_var, units=time_units, calendar=time_calendar)

# Determine the range of the time variable using Python's built-in min and max functions
time_min = min(time_dates)
time_max = max(time_dates)

print(f"Time range: {time_min} to {time_max}")

# Close the dataset
dataset.close()
