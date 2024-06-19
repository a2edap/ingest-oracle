import xarray as xr
from tsdat import IngestPipeline


class NoaaCnsTemp(IngestPipeline):

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        pass
