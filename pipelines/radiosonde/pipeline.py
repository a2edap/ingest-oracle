import xarray as xr

# import matplotlib.pyplot as plt
from tsdat import IngestPipeline  # , get_start_date_and_time_str, get_filename

# from utils import format_time_xticks


class Radiosonde(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        pass
