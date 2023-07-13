#!/usr/bin/env python
# coding: utf-8
# pylint: disable=C0116, C0114

import os
import sys
import pickle
import logging
from datetime import datetime

import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def read_data(filename):
    # pylint: disable=C0103
    s3_endpoint_url = os.getenv("S3_ENDPOINT_URL")
    if s3_endpoint_url is not None:
        options = {"client_kwargs": {"endpoint_url": s3_endpoint_url}}
        df = pd.read_parquet(filename, storage_options=options)
        return df

    df = pd.read_parquet(filename)
    return df


def prepare_data(df, categorical):
    # pylint: disable=C0103
    df["duration"] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df["duration"] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype("int").astype("str")

    return df


def dt(hour, minute, second=0):
    # pylint: disable=C0103
    return datetime(2022, 1, 1, hour, minute, second)


def get_input_path(year, month):
    # pylint: disable=C0209
    default_input_pattern = (
        "s3://nyc-duration/taxi_type=fhv/" "year={:04d}/month={:02d}/input.parquet"
    ).format(year, month)
    input_pattern = os.getenv("INPUT_FILE_PATTERN", default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    # pylint: disable=C0209
    default_output_pattern = (
        "s3://nyc-duration/taxi_type=fhv/"
        "year={:04d}/month={:02d}/predictions.parquet"
    ).format(year, month)
    output_pattern = os.getenv("OUTPUT_FILE_PATTERN", default_output_pattern)
    return output_pattern.format(year=year, month=month)


def save_data(df, output_file):
    # pylint: disable=C0103
    s3_endpoint_url = os.getenv("S3_ENDPOINT_URL")
    if s3_endpoint_url is not None:
        options = {"client_kwargs": {"endpoint_url": s3_endpoint_url}}
        df.to_parquet(
            output_file,
            engine="pyarrow",
            compression=None,
            index=False,
            storage_options=options,
        )
        return

    df.to_parquet(output_file, engine="pyarrow", index=False)


def main(year, month):
    # pylint: disable=C0103
    input_file = get_input_path(year, month)
    logging.debug("Input file: %s", input_file)
    output_file = get_output_path(year, month)
    logging.debug("Output file: %s", output_file)

    with open("model.bin", "rb") as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ["PULocationID", "DOLocationID"]

    df = read_data(input_file)
    df = prepare_data(df, categorical)
    df["ride_id"] = f"{year:04d}/{month:02d}_" + df.index.astype("str")
    logging.info("The number of rows in the expeted dataframe is: %d", len(df))

    dicts = df[categorical].to_dict(orient="records")
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    logging.debug("Predicted result: %r", y_pred)

    logging.info("predicted mean duration: %f", y_pred.mean())
    logging.info("predicted sum duration: %f", y_pred.sum())

    df_result = pd.DataFrame()
    df_result["ride_id"] = df["ride_id"]
    df_result["predicted_duration"] = y_pred

    save_data(df_result, output_file)


if __name__ == "__main__":
    INPUT_YEAR = int(sys.argv[1])
    INPUT_MONTH = int(sys.argv[2])

    main(INPUT_YEAR, INPUT_MONTH)
