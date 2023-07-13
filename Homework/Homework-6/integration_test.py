import pandas as pd
import os
from batch import dt, read_data, get_input_path, get_output_path

data = [
    (None, None, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2), dt(1, 10)),
    (1, 2, dt(2, 2), dt(2, 3)),
    (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
    (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),     
    ]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df_input = pd.DataFrame(data, columns=columns)

year = 2022
month = 1
input_path = get_input_path(2022, 1)
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL","http://localhost:4566")
options = {
    'client_kwargs': {
        'endpoint_url': S3_ENDPOINT_URL
    }
}


df_input.to_parquet(
    input_path,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)

os.system(f"python batch.py {year} {month}")

output_path = get_output_path(2022, 1)
output_df = read_data(output_path)
total_duration = output_df["predicted_duration"].sum()
expected_total_duration = 31.5

assert (total_duration - expected_total_duration) < 0.01
