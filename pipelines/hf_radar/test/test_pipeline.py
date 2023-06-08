import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_hf_radar_6km_pipeline():
    config_path = Path("pipelines/hf_radar/config/pipeline_6km.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "2012-01"
    expected_file = "pipelines/hf_radar/test/data/expected/sccoos.hf_radar-6km.b1.20120101.000000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)


def test_hf_radar_2km_pipeline():
    config_path = Path("pipelines/hf_radar/config/pipeline_2km.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "2012-01"
    expected_file = "pipelines/hf_radar/test/data/expected/sccoos.hf_radar-2km.b1.20120101.000000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
