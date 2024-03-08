import os
import xarray as xr
import matplotlib.pyplot as plt
from cmocean.cm import amp_r, dense, haline

from tsdat import IngestPipeline, get_start_date_and_time_str, get_filename


class CDIPWaveBuoy(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset before qc is applied

        # Remove downloaded file from disk space
        os.remove(dataset.attrs.pop("fname"))

        # Reset dataset title to original
        dataset.attrs["title"] = dataset.attrs.pop("cdip_title")
        # Drop tsdat's "description" attribute ("summary" exists)
        dataset.attrs.pop("description")
        # Set station name
        if hasattr(dataset, "cdip_station_id"):
            dataset.attrs["dataset_name"] = dataset.attrs["cdip_station_id"]
        elif hasattr(dataset, "id"):
            dataset.attrs["dataset_name"] = dataset.attrs["id"][5:8]
            dataset.attrs["cdip_station_id"] = dataset.attrs["id"][5:8]
        # Reset datastream
        dataset.attrs["datastream"] = dataset.attrs["datastream"].replace(
            "000", dataset.attrs["cdip_station_id"]
        )

        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area

        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        ds = dataset
        loc = dataset.attrs["location_id"]
        datastream: str = dataset.attrs["datastream"]

        date, time = get_start_date_and_time_str(dataset)

        plt.style.use("default")  # clear any styles that were set before
        plt.style.use("shared/styling.mplstyle")

        with self.storage.uploadable_dir(datastream) as tmp_dir:
            fig, axs = plt.subplots(nrows=3)

            # Plot Wave Heights
            c2 = amp_r(0.50)
            ds["significant_wave_height"].plot(ax=axs[0], c=c2, label=r"H$_{sig}$")
            axs[0].legend(bbox_to_anchor=(1, -0.10), ncol=3)
            axs[0].set_ylabel("Wave Height (m)")

            # Plot Wave Periods
            c1, c2 = dense(0.3), dense(0.6)
            ds["average_wave_period"].plot(ax=axs[1], c=c1, label=r"T$_{mean}$")
            ds["dominant_wave_period"].plot(ax=axs[1], c=c2, label=r"T$_{peak}$")
            axs[1].legend(bbox_to_anchor=(1, -0.10), ncol=3)
            axs[1].set_ylabel("Wave Period (s)")

            # Plot Wave Directions
            c1 = haline(0.5)
            ds["dominant_wave_direction"].plot(ax=axs[2], c=c1, label=r"D$_{peak}$")
            axs[2].legend(bbox_to_anchor=(1, -0.10), ncol=2)
            axs[2].set_ylabel("Wave Direction (deg)")

            # c1 = haline(0.9)
            # ds["sea_surface_temperature"].plot(ax=axs[3], c=c1, label=r"Sea Surface$")
            # axs[3].legend(bbox_to_anchor=(1, -0.10), ncol=2)
            # axs[3].set_ylabel("Temperature (deg C)")

            for i in range(len(axs)):
                axs[i].set_xlabel("Time (UTC)")

            plot_file = get_filename(ds, title="wave_data_plots", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)
