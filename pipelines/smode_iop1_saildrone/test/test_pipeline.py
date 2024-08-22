import xarray as xr
from pathlib import Path
from utils.a2e_tsdat import PipelineConfig, assert_close


# Commented out the test due to the output file's large size, which makes it too difficult to upload.
def test_smode_iop1_saildrone_pipeline():
    config_path = Path("pipelines/smode_iop1_saildrone/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/smode_iop1_saildrone/test/data/input/subset_SMODE_PFC_saildrone_nonadcp_1062.nc"
    expected_file = "pipelines/smode_iop1_saildrone/test/data/expected/smode.saildrone1.1062.a1.20211024.000000.pilot.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
