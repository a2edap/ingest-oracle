import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


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
