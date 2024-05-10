import os
import xarray as xr
import matplotlib.pyplot as plt
from tsdat import IngestPipeline, get_start_date_and_time_str, get_filename

from utils import format_time_xticks


class SCCOOS_HFRadar(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset before qc is applied

        # Remove raw file from disk space
        os.remove(f"data_{dataset.qualifier}.nc")

        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area

        # Drop QC for grid information
        if "qc_wgs84" in dataset:
            dataset = dataset.drop("qc_wgs84")
        # Update history
        dataset.attrs["history"] = (
            dataset.attrs.pop("History") + "\n" + dataset.attrs.pop("history")
        )
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        # (Optional, recommended) Create plots.
        location = self.dataset_config.attrs.location_id
        datastream: str = self.dataset_config.attrs.datastream

        date, time = get_start_date_and_time_str(dataset)

        plt.style.use("default")  # clear any styles that were set before
        plt.style.use("shared/styling.mplstyle")

        with self.storage.uploadable_dir() as tmp_dir:
            fig, ax = plt.subplots(1, 2, figsize=(12, 10))
            h1 = ax[0].pcolormesh(
                dataset["longitude"],
                dataset["latitude"],
                dataset["u"].mean("time"),
                cmap="coolwarm",
                vmin=-1,
                vmax=1,
            )
            ax[0].set(
                xlabel="Longitude [deg E]",
                ylabel="Latitude [deg N]",
                title="U direction",
            )

            h2 = ax[1].pcolormesh(
                dataset["longitude"],
                dataset["latitude"],
                dataset["v"].mean("time"),
                cmap="coolwarm",
                vmin=-1,
                vmax=1,
            )
            ax[1].set(
                xlabel="Longitude [deg E]",
                ylabel="Latitude [deg N]",
                title="V direction",
            )
            fig.colorbar(h2, ax=ax[1], label="Velocity [m/s]")

            fig.suptitle(f"Monthly Average for {date}")
            plot_file = get_filename(dataset, title="surface_velocity", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)
