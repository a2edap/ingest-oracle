import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_radiosonde_USM00072293_pipeline():
    config_path = Path("pipelines/radiosonde/config/pipeline_USM00072293.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/radiosonde/test/data/input/USM00072293.2019.01.01"
    expected_file = (
        "pipelines/radiosonde/test/data/expected/san.radio.b0.20190101.110000.nc"
    )

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)


def test_radiosonde_USM00072493_pipeline():
    config_path = Path("pipelines/radiosonde/config/pipeline_USM00072493.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/radiosonde/test/data/input/USM00072493.2019.01.01"
    expected_file = (
        "pipelines/radiosonde/test/data/expected/oak.radio.b0.20190101.110000.nc"
    )

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
