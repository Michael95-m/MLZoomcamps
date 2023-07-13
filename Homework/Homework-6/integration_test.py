# pylint: disable=C0114

import os

import pandas as pd

from batch import read_data, get_input_path, get_output_path
from utils import get_test_data

data, columns = get_test_data()
df_input = pd.DataFrame(data, columns=columns)

YEAR = 2022
MONTH = 1
input_path = get_input_path(2022, 1)
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://localhost:4566")
options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}


df_input.to_parquet(
    input_path, engine="pyarrow", compression=None, index=False, storage_options=options
)

os.system(f"python batch.py {YEAR} {MONTH}")

output_path = get_output_path(2022, 1)
output_df = read_data(output_path)
total_duration = output_df["predicted_duration"].sum()
EXPECTED_TOTAL_DURATION = 31.5

assert (total_duration - EXPECTED_TOTAL_DURATION) < 0.01
