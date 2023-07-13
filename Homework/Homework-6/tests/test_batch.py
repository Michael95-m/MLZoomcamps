# pylint: disable=C0114, C0116

import pandas as pd

from batch import dt, prepare_data
from utils import get_test_data


def test_prepare_data():
    # pylint: disable=C0103

    data, columns = get_test_data()
    categorical = ["PULocationID", "DOLocationID"]

    df = pd.DataFrame(data, columns=columns)

    actual_data = prepare_data(df, categorical).to_dict(orient="records")
    expected_data = [
        {
            "PULocationID": "-1",
            "DOLocationID": "-1",
            "tpep_pickup_datetime": dt(1, 2),
            "tpep_dropoff_datetime": dt(1, 10),
            "duration": 8.0,
        },
        {
            "PULocationID": "1",
            "DOLocationID": "-1",
            "tpep_pickup_datetime": dt(1, 2),
            "tpep_dropoff_datetime": dt(1, 10),
            "duration": 8.0,
        },
        {
            "PULocationID": "1",
            "DOLocationID": "2",
            "tpep_pickup_datetime": dt(2, 2),
            "tpep_dropoff_datetime": dt(2, 3),
            "duration": 1.0,
        },
    ]
    assert expected_data == actual_data
