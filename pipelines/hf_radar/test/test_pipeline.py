import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


# DEVELOPER: Update paths to your configuration(s), test input(s), and expected test
# results files.
def test_hf_radar_pipeline():
    config_path = Path("pipelines/hf_radar/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/hf_radar/test/data/input/sccoos_data.csv"
    expected_file = (
        "pipelines/hf_radar/test/data/expected/abc.example.a1.20220424.000000.nc"
    )

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
