import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close
import os


# DEVELOPER: Update paths to your configuration(s), test input(s), and expected test
# results files.
def test_noaa_weber_wuertz_temp_pipeline():
    config_path = Path("pipelines/noaa_weber_wuertz_temp/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/noaa_weber_wuertz_temp/test/data/input/ca_data.csv"
    expected_file = "pipelines/noaa_weber_wuertz_temp/test/data/expected/abc.example.a1.20220424.000000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)


def test_noaa_weber_wuertz_wind_tci_pipeline():
    config_path = Path("pipelines/noaa_weber_wuertz_wind/config/pipeline_tci.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/noaa_weber_wuertz_wind/test/data/input/tci19043.00w.txt"
    expected_file = "pipelines/noaa_weber_wuertz_wind/test/data/expected/tci.noaa_weber_wuertz_wind.b0.20190212.000017.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)


def test_noaa_weber_wuertz_wind_ove_pipeline():
    config_path = Path("pipelines/noaa_weber_wuertz_wind/config/pipeline_ove.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/noaa_weber_wuertz_wind/test/data/input/ove21008.05w.txt"
    expected_file = "pipelines/noaa_weber_wuertz_wind/test/data/expected/ove.noaa_weber_wuertz_wind.b0.20210108.050005.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
