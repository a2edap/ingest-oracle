import xarray as xr
from pathlib import Path

from utils.a2e_tsdat import PipelineConfig, TransformationPipeline, assert_close


def test_iop_saildrone_pipeline():
    config_path = Path("pipelines/iop_saildrone/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/iop_saildrone/test/data/input/1026_5min.nc"
    expected_file = "pipelines/iop_saildrone/test/data/expected/smode.saildrone1.1026.a1.20221006.071928.iop1.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
