from tsdat.tstring import TEMPLATE_REGISTRY

TEMPLATE_REGISTRY["datastream"] = (
    "{location_id}[.{instrument}].{dataset_name}.{z_id}.{data_level}"
)

from tsdat import *
