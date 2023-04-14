import numpy as np
import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


# CDIP "real time" data
def test_cdip_pipeline_rt():
    config_path = Path("pipelines/cdip/config/pipeline_realtime.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "201"
    expected_file = "pipelines/cdip/test/data/expected/cdip.201.c1.20220201.000000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore

    time = slice(np.datetime64("2022-02-01"), np.datetime64("2022-05-01"))
    dataset = dataset.sel(time=time, sst_time=time, gps_time=time, dwr_time=time)

    assert_close(dataset, expected, check_attrs=False)


# CDIP "historic" data
def test_cdip_pipeline_hist():
    config_path = Path("pipelines/cdip/config/pipeline_historic.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "181"
    expected_file = "pipelines/cdip/test/data/expected/cdip.181.c1.20200201.000000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore

    time = slice(np.datetime64("2020-02-01"), np.datetime64("2020-05-01"))
    dataset = dataset.sel(time=time, sst_time=time, gps_time=time, dwr_time=time)

    assert_close(dataset, expected, check_attrs=False)
