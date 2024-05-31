import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_noaa_weber_wuertz_temp_ove_pipeline():
    config_path = Path("pipelines/noaa_weber_wuertz_temp/config/pipeline_ove.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/noaa_weber_wuertz_temp/test/data/input/ove21010.05t.txt"
    expected_file = "pipelines/noaa_weber_wuertz_temp/test/data/expected/ove.noaa_weber_wuertz_temp.b0.20210110.055553.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
