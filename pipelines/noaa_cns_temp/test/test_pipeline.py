import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_noaa_cns_temp_nps_pipeline():
    config_path = Path("pipelines/noaa_cns_temp/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/noaa_cns_temp/test/data/input/nps21007.05w.txt"
    expected_file = "pipelines/noaa_cns_temp/test/data/expected/nps.noaa_cns_temp.b0.20210107.050415.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
