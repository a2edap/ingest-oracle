import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from mhkit.wave import resource as wr
from mhkit.wave.io.cdip import request_netCDF

station = '201'
nc = request_netCDF(station, data_type='realtime')  # 'realtime' vs 'historic'
ds = xr.open_dataset(xr.backends.NetCDF4DataStore(nc))

#ds = xr.open_dataset('201p1_rt.nc')
time = slice(np.datetime64('2022-02-01'), np.datetime64('2022-05-21'))
ds_cdip = ds.sel(waveTime=time, sstTime=time, gpsTime=time, dwrTime=time)

Te = ds_cdip['waveTa'].data * 0
Tp = ds_cdip['waveTa'].data * 0
for i in range(len(ds_cdip['waveTime'])):
    Te[i] = wr.energy_period(ds_cdip['waveEnergyDensity'][i].to_pandas()).values.squeeze()
    Tp[i] = wr.peak_period(ds_cdip['waveEnergyDensity'][i].to_dataframe('Tp').drop(labels=['waveTime','metaDeployLatitude','metaDeployLongitude'], axis=1)
                           ).values.squeeze()

ds_cdip['waveTe'] = xr.DataArray(Te,
                                 dims=['waveTime'],
                                 attrs={'units': 's',
                                        'long_name': 'wave energy period',
                                        'standard_name': 'sea_surface_wave_mean_period_from_variance_spectral_density_inverse_frequency_moment',
                                        'additional_processing': 'Calculated from the full-spectrum, buoy-returned energy density values.'}
                                 )

# Check MHKiT calculations against buoy saved data
plt.figure()
plt.plot(ds_cdip.waveTime, Te)
plt.plot(ds_cdip.waveTime, Tp)
plt.plot(ds_cdip.waveTime, ds_cdip.waveTp)

#ds_cdip.to_netcdf('SIO_waves_data.20220201.nc')