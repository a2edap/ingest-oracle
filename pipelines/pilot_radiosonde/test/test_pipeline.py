import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_pilot_radiosonde_pipeline():
    config_path = Path("pipelines/pilot_radiosonde/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/pilot_radiosonde/test/data/input/S-MODE_PFC_OC2108A_radiosonde_001.nc"
    expected_file = "pipelines/pilot_radiosonde/test/data/expected/abc.example.a1.20220424.000000.nc"

    dataset = pipeline.run([test_file])
    # expected: xr.Dataset = xr.open_dataset(expected_file)
    # assert_close(dataset, expected, check_attrs=False)